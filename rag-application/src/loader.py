from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader


def load_documents(data_path: str = "data/"):
    """
    data/ folder ke andar sari PDF files load karta hai
    """
    loader = DirectoryLoader(
        data_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    print(f"{len(documents)} pages loaded from {data_path}")
    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(docs[0].page_content[:300])  # pehle document ka preview