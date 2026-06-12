# AI Resume Matcher 🎯

An AI-powered Resume Screening System using **LangChain**, **ChromaDB (RAG)**, and **Gemini 2.5 Flash**.

## Features
- 📄 Parse multiple PDF resumes
- 🧠 Embed resumes into a ChromaDB vector store
- 🔍 MMR retrieval + CrossEncoder reranking
- 🤖 AI ATS scoring (0–100) ranked by relevance
- 💬 Natural language Q&A about shortlisted candidates
- 🖥️ FastAPI REST backend
- 📊 Streamlit HR Dashboard

---

## Project Structure

```
resume_matcher/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app (endpoints)
│   ├── pipeline.py      # Singleton RAG pipeline manager
│   └── schemas.py       # Pydantic request/response models
├── frontend/
│   └── streamlit_app.py # Streamlit HR Dashboard
├── src/                 # Core LangChain pipeline modules
│   ├── embeddings.py
│   ├── llm.py
│   ├── pdf_loader.py
│   ├── qa_engine.py
│   ├── rag_chain.py
│   ├── reranker.py
│   ├── resume_loader.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
├── data/
│   └── resumes/         # Place PDF resumes here
├── chroma_db/           # Auto-generated vector store
├── .env                 # GOOGLE_API_KEY=...
├── requirements.txt
├── run_backend.bat      # One-click FastAPI launcher (Windows)
└── run_frontend.bat     # One-click Streamlit launcher (Windows)
```

---

## Setup

### 1. Create & activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API key
Edit `.env`:
```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Add resumes
Place PDF resume files in `data/resumes/`.

---

## Running

### Option A — Batch scripts (Windows)
Open **two terminals**:

**Terminal 1 — Backend:**
```
run_backend.bat
```

**Terminal 2 — Frontend:**
```
run_frontend.bat
```

### Option B — Manual
```bash
# Terminal 1
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2
streamlit run frontend/streamlit_app.py
```

### URLs
| Service | URL |
|---|---|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/candidates` | List uploaded resume files |
| POST | `/upload-resumes` | Upload PDF resumes |
| POST | `/match` | Run AI match against a JD |
| POST | `/qa` | Q&A about shortlisted candidates |

---

## Tech Stack
- **LangChain** — document loading, RAG pipeline
- **ChromaDB** — vector database (persisted locally)
- **HuggingFace** — `all-MiniLM-L6-v2` embeddings
- **CrossEncoder** — `ms-marco-MiniLM-L-6-v2` reranker
- **Google Gemini 2.5 Flash** — LLM for ATS scoring + Q&A
- **FastAPI** — REST API backend
- **Streamlit** — HR dashboard frontend
