from src.resume_loader import load_resumes
from src.text_splitter import split_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store
from src.retriever import get_retriever
from src.llm import get_llm
from src.rag_chain import build_rag_chain

# 1. Load resumes
documents = load_resumes("data/resumes")

# 2. Split into chunks
chunks = split_documents(documents)

# 3. Embeddings
embedding_model = get_embedding_model()

# 4. Vector store
vector_store = create_vector_store(chunks, embedding_model)

# 5. Retriever (MMR)
retriever = get_retriever(vector_store)

# 6. LLM
llm = get_llm()

# 7. Prompt
prompt = build_rag_chain()

# ----------------------------
# QUERY
# ----------------------------
question = "Who has Linux experience?"

# 8. Retrieve docs
docs = retriever.invoke(question)

# ----------------------------
# STEP: DEDUPLICATION (IMPORTANT FIX)
# ----------------------------
unique_docs = {}
for doc in docs:
    source = doc.metadata.get("source", "unknown")
    if source not in unique_docs:
        unique_docs[source] = doc

docs = list(unique_docs.values())

# ----------------------------
# DEBUG: show retrieved resumes
# ----------------------------
print("\n--- UNIQUE RETRIEVED RESUMES ---")

for i, doc in enumerate(docs):
    print(f"\n[{i+1}] {doc.metadata.get('source')}")
    print(doc.page_content[:250])

# ----------------------------
# BUILD CONTEXT
# ----------------------------
context = "\n\n".join(
    f"""
Resume File: {doc.metadata.get('source', 'unknown')}
Content:
{doc.page_content}
""".strip()
    for doc in docs
)

# ----------------------------
# LLM INVOKE
# ----------------------------
messages = prompt.invoke({
    "context": context,
    "question": question
})

response = llm.invoke(messages)

print("\n--- FINAL ANSWER ---\n")
print(response.content)