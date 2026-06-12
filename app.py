from src.resume_loader import load_resumes
from src.text_splitter import split_documents

folder_path = "data/resumes"

documents = load_resumes(folder_path)

chunks = split_documents(documents)

print(f"Total Documents: {len(documents)}")
print(f"Total Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:5], start=1):
    print(f"Chunk {i}")
    print(chunk.page_content[:300])
    print("-" * 50)