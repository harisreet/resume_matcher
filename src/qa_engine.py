from langchain_core.prompts import ChatPromptTemplate

# Q&A prompt (separate from ATS)
qa_prompt = ChatPromptTemplate.from_template("""
You are a Resume Shortlisted Candidate Q&A assistant.

RULES:
- Answer ONLY using shortlisted resumes
- Mention resume file name
- Compare candidates if needed
- Do NOT use external knowledge

SHORTLISTED RESUMES:
{context}

QUESTION:
{question}
""")

def build_shortlist_context(docs):
    return "\n\n====================\n\n".join(
        f"""
Resume File: {doc.metadata.get('source', 'unknown')}
Content:
{doc.page_content}
""".strip()
        for doc in docs
    )

def ask_shortlisted_candidates(question, shortlisted_docs, llm):

    context = build_shortlist_context(shortlisted_docs)

    messages = qa_prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    return response.content

