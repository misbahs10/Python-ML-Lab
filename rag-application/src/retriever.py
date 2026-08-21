from embeddings import load_vectorstore #type: ignore


def get_retriever(k: int = 3):
    """
    Vectorstore se ek retriever banata hai jo top-k relevant chunks return karta hai
    """
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever


def retrieve_relevant_chunks(query: str, k: int = 3):
    """
    Diye gaye query ke liye sabse relevant chunks nikalta hai
    """
    retriever = get_retriever(k=k)
    results = retriever.invoke(query)
    return results


if __name__ == "__main__":
    query = "What is machine learning?"
    results = retrieve_relevant_chunks(query)

    print(f"Query: {query}\n")
    print(f"--- Top {len(results)} relevant chunks ---")
    for i, r in enumerate(results):
        print(f"\n[{i+1}] {r.page_content[:250]}...")
        print(f"    Source: {r.metadata.get('source')}, Page: {r.metadata.get('page')}")