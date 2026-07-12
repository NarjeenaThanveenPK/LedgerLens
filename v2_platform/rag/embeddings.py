from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rag.document_loader import load_documents, split_documents
import os

VECTORSTORE_PATH = "vectorstore/faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_vectorstore():
    print("Loading documents...")
    docs = load_documents()
    
    if not docs:
        print("No documents found.")
        return None
    
    print("Splitting into chunks...")
    chunks = split_documents(docs)
    
    print(f"Building embeddings using {EMBEDDING_MODEL}...")
    print("First run takes 3-5 minutes...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    
    print(f"Vectorstore saved to {VECTORSTORE_PATH}")
    print(f"Total chunks indexed: {len(chunks)}")
    
    return vectorstore


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    print("Vectorstore loaded.")
    return vectorstore


def get_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        return load_vectorstore()
    else:
        return build_vectorstore()


if __name__ == "__main__":
    vs = build_vectorstore()
    if vs:
        print("\nVectorstore ready.")