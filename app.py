from src.resume_loader import load_resumes

folder_path = "data/resumes"

documents = load_resumes(folder_path)

print(f"Total Pages Loaded: {len(documents)}\n")

for doc in documents:
    print("Resume:", doc.metadata["source"])
    print(doc.page_content[:200])
    print("-" * 50)