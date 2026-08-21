import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "vectorstore"


def get_embedding_model():
    """
    Free, local HuggingFace embedding model load karta hai
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(chunks, persist_directory: str = PERSIST_DIR):
    """
    Chunks ko embeddings mein convert karke ChromaDB mein save karta hai
    """
    embedding_model = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    print(f"Vectorstore created and saved to '{persist_directory}'")
    return vectorstore


def load_vectorstore(persist_directory: str = PERSIST_DIR):
    """
    Pehle se saved vectorstore ko load karta hai (dobara embed nahi karna parta)
    """
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    return vectorstore


if __name__ == "__main__":
    from loader import load_documents #type: ignore
    from splitter import split_documents #type: ignore

    docs = load_documents()
    chunks = split_documents(docs)
    vectorstore = create_vectorstore(chunks)

    # quick test: similarity search
    results = vectorstore.similarity_search("What is RAG?", k=2)
    print("\n--- Top matching chunks for 'What is RAG?' ---")
    for i, r in enumerate(results):
        print(f"\n[{i+1}] {r.page_content[:200]}...")