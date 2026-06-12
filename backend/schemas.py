from pydantic import BaseModel
from typing import List, Optional


# ── Requests ──────────────────────────────────────────────────────────────────

class MatchRequest(BaseModel):
    job_description: str
    top_k: Optional[int] = 5          # how many candidates to return


class QARequest(BaseModel):
    question: str
    shortlisted_files: List[str]       # list of resume filenames to search over


# ── Responses ─────────────────────────────────────────────────────────────────

class CandidateMatch(BaseModel):
    rank: int
    resume_file: str
    match_score: int                   # 0–100
    matched_skills: List[str]
    missing_skills: List[str]
    evidence: str
    raw_text_preview: Optional[str] = None


class MatchResponse(BaseModel):
    job_description: str
    total_resumes_searched: int
    candidates: List[CandidateMatch]


class QAResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]


class UploadResponse(BaseModel):
    uploaded: List[str]
    total_resumes: int
    message: str


class CandidatesResponse(BaseModel):
    resumes: List[str]
    count: int
