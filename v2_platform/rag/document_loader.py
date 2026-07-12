from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

PROCESSED_FOLDER = "data/processed"

def load_documents():
    docs = []
    
    if not os.path.exists(PROCESSED_FOLDER):
        print(f"Folder not found: {PROCESSED_FOLDER}")
        return []
    
    for filename in os.listdir(PROCESSED_FOLDER):
        if not filename.endswith(".txt"):
            continue
        
        filepath = os.path.join(PROCESSED_FOLDER, filename)
        
        try:
            loader = TextLoader(filepath, encoding="utf-8")
            documents = loader.load()
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            continue
        
        parts = filename.replace(".txt", "").split("_")
        company = parts[0].capitalize()
        year = parts[2] if len(parts) > 2 else "unknown"
        
        for doc in documents:
            doc.metadata["company"] = company
            doc.metadata["year"] = year
            doc.metadata["source"] = filename
            doc.metadata["display"] = f"{company} 10-K {year}"
        
        docs.extend(documents)
    
    print(f"Loaded {len(docs)} documents")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    print(f"\nSample chunk:")
    print(chunks[0].page_content[:300])
    print(f"\nMetadata: {chunks[0].metadata}")