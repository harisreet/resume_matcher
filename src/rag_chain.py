from langchain_core.prompts import ChatPromptTemplate

def build_rag_chain():
    return ChatPromptTemplate.from_template("""
You are a strict resume screening assistant.

RULES:
- Answer ONLY from provided resumes
- Do NOT assume anything
- If not found, say "Not found in resumes"
- Always mention resume filename

OUTPUT FORMAT:
Candidate:
Evidence:
Resume File:

Context:
{context}

Question:
{question}
""")