import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from retriever import get_retriever #type: ignore

load_dotenv()

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information in the documents to answer that."

Context:
{context}

Question: {question}

Answer:"""


def get_llm():
    """
    Groq ka free, fast LLM load karta hai
    """
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )


def format_docs(docs):
    """
    Retrieved chunks ko ek single text block mein combine karta hai
    """
    return "\n\n".join(doc.page_content for doc in docs)


def ask_question(query: str, k: int = 3):
    """
    Poora RAG pipeline: retrieve -> prompt -> LLM -> answer
    """
    retriever = get_retriever(k=k)
    relevant_docs = retriever.invoke(query)
    context = format_docs(relevant_docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = get_llm()

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": query})

    return response.content, relevant_docs


if __name__ == "__main__":
    query = "What is RAG and why is it useful?"
    answer, sources = ask_question(query)

    print(f"Question: {query}\n")
    print(f"Answer: {answer}\n")
    print("--- Sources used ---")
    for i, doc in enumerate(sources):
        print(f"[{i+1}] {doc.metadata.get('source')} (page {doc.metadata.get('page')})")