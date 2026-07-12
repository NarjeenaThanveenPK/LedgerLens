from rag.embeddings import get_vectorstore


def get_retriever(k=5):
    vs = get_vectorstore()
    return vs.as_retriever(search_kwargs={"k": k})


def retrieve_context(query, k=5):
    retriever = get_retriever(k=k)
    docs = retriever.invoke(query)
    
    context_parts = []
    sources = []
    seen = set()
    
    for i, doc in enumerate(docs):
        context_parts.append(doc.page_content)
        
        display = doc.metadata.get("display", "Unknown")
        if display not in seen:
            seen.add(display)
            sources.append({
                "company": doc.metadata.get("company", "Unknown"),
                "year": doc.metadata.get("year", "Unknown"),
                "display": display,
                "chunk_index": i + 1
            })
    
    context = "\n\n---\n\n".join(context_parts)
    return context, sources


if __name__ == "__main__":
    print("Testing retriever...")
    query = "What was Apple revenue growth?"
    context, sources = retrieve_context(query)
    print(f"\nRetrieved {len(sources)} sources:")
    for s in sources:
        print(f"  - {s['display']}")
    print(f"\nContext preview:\n{context[:400]}")