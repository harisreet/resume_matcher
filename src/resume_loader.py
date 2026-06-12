import os
from langchain_community.document_loaders import PyPDFLoader


def load_resumes(folder_path):
    all_documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):

            pdf_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(pdf_path)

            documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = file

            all_documents.extend(documents)

    return all_documents