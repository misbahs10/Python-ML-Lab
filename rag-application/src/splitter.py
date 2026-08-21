from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size: int = 500, chunk_overlap: int = 50):
    """
    Documents ko chote overlapping chunks mein todta hai
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"{len(documents)} documents split into {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    from loader import load_documents #type: ignore

    docs = load_documents()
    chunks = split_documents(docs)

    print("\n--- Sample chunk ---")
    print(chunks[0].page_content)
    print("\nMetadata:", chunks[0].metadata)