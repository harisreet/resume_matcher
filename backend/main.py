"""
main.py — FastAPI backend for Resume Matcher
Run: uvicorn backend.main:app --reload
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    MatchRequest, MatchResponse, CandidateMatch,
    QARequest, QAResponse,
    UploadResponse, CandidatesResponse,
)
from backend import pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

RESUMES_DIR = Path("data/resumes")
RESUMES_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Resume Matcher API",
    description="AI-powered Resume Screening System using LangChain + RAG",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "Resume Matcher API"}


@app.get("/candidates", response_model=CandidatesResponse)
def list_candidates():
    """Return all uploaded resume filenames."""
    resumes = pipeline.list_resumes()
    return CandidatesResponse(resumes=resumes, count=len(resumes))


@app.post("/upload-resumes", response_model=UploadResponse)
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Upload one or more PDF resumes.
    Saves them to data/resumes/ and returns the updated file list.
    """
    uploaded = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are accepted. Got: {file.filename}"
            )
        dest = RESUMES_DIR / file.filename
        with dest.open("wb") as f:
            shutil.copyfileobj(file.file, f)
        uploaded.append(file.filename)
        logger.info(f"Uploaded: {file.filename}")

    all_resumes = pipeline.list_resumes()
    return UploadResponse(
        uploaded=uploaded,
        total_resumes=len(all_resumes),
        message=f"Successfully uploaded {len(uploaded)} file(s).",
    )


@app.post("/match", response_model=MatchResponse)
def match_resumes(req: MatchRequest):
    """
    Run the full RAG pipeline against a Job Description.
    Returns ranked candidates with match scores.
    """
    if not req.job_description.strip():
        raise HTTPException(status_code=400, detail="job_description cannot be empty.")

    resumes = pipeline.list_resumes()
    if not resumes:
        raise HTTPException(
            status_code=404,
            detail="No resumes found. Please upload PDFs first."
        )

    logger.info(f"Running match for JD ({len(req.job_description)} chars) against {len(resumes)} resumes…")
    results = pipeline.run_match(req.job_description, top_k=req.top_k or 5)

    candidates = [
        CandidateMatch(
            rank=c.get("rank", i + 1),
            resume_file=c.get("resume_file", "unknown.pdf"),
            match_score=int(c.get("match_score", 0)),
            matched_skills=c.get("matched_skills", []),
            missing_skills=c.get("missing_skills", []),
            evidence=c.get("evidence", ""),
            raw_text_preview=c.get("raw_text_preview"),
        )
        for i, c in enumerate(results)
    ]

    return MatchResponse(
        job_description=req.job_description,
        total_resumes_searched=len(resumes),
        candidates=candidates,
    )


@app.post("/qa", response_model=QAResponse)
def qa_shortlisted(req: QARequest):
    """
    Answer a natural-language question about shortlisted candidates.
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question cannot be empty.")
    if not req.shortlisted_files:
        raise HTTPException(status_code=400, detail="shortlisted_files cannot be empty.")

    logger.info(f"Q&A: '{req.question}' over {req.shortlisted_files}")
    result = pipeline.run_qa(req.question, req.shortlisted_files)

    return QAResponse(
        question=req.question,
        answer=result["answer"],
        sources=result["sources"],
    )
