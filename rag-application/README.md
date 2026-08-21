# 📄 RAG Application — Document Q&A AI

A Retrieval-Augmented Generation (RAG) application that answers questions based on the content of your own documents. Instead of relying only on a language model's training data, this app retrieves relevant chunks from your PDFs and uses them as grounded context to generate accurate, source-backed answers.

## 🚀 Features

- Load and process PDF documents
- Split documents into semantically meaningful chunks
- Generate embeddings using a free, local HuggingFace model
- Store and search embeddings using ChromaDB (vector database)
- Retrieve the most relevant chunks for any question
- Generate grounded answers using Groq's fast, free LLM
- Simple command-line chat interface (`main.py`)
- REST API built with FastAPI (`api.py`), with interactive Swagger docs

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Framework | LangChain |
| Embeddings | HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| LLM | Groq (`openai/gpt-oss-20b`) |
| API | FastAPI |
| Package Manager | uv |

## 📂 Project Structure

```
rag-application/
├── data/                # Source PDF documents
├── vectorstore/         # ChromaDB persisted vector store
├── src/
│   ├── loader.py         # Loads PDF documents
│   ├── splitter.py       # Splits documents into chunks
│   ├── embeddings.py      # Creates embeddings & vector store
│   ├── retriever.py       # Retrieves relevant chunks for a query
│   └── qa_chain.py        # Combines retrieval + LLM to generate answers
├── main.py               # Command-line chat interface
├── api.py                # FastAPI REST API
├── .env                  # API keys (not committed)
└── pyproject.toml        # Project dependencies
```

## ⚙️ How It Works

1. **Indexing (done once):** Documents are loaded, split into chunks, converted into embeddings, and stored in ChromaDB.
2. **Querying (every question):** The user's question is embedded, the most similar chunks are retrieved from ChromaDB, and those chunks are passed to the LLM along with the question to generate a grounded answer.

## 📦 Setup

1. Clone the repository and install dependencies:
```bash
uv venv
uv add langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters langchain-huggingface langchain-groq chromadb pypdf python-dotenv sentence-transformers fastapi uvicorn
```

2. Add your Groq API key to a `.env` file:
```
GROQ_API_KEY=your_key_here
```

3. Place your PDF file(s) inside the `data/` folder.

4. Build the vector store:
```bash
uv run src/embeddings.py
```

## ▶️ Usage

**Command-line chat:**
```bash
uv run main.py
```

**REST API:**
```bash
uv run uvicorn api:app --reload
```
Then open `http://127.0.0.1:8000/docs` to test the `/ask` endpoint interactively.

Example request to `/ask`:
```json
{
  "question": "What is RAG?",
  "k": 3
}
```

Example response:
```json
{
  "question": "What is RAG?",
  "answer": "Retrieval-Augmented Generation (RAG) is a technique that combines a language model with an external knowledge source...",
  "sources": [
    { "source": "data/sample.pdf", "page": 1 }
  ]
}
```

## 🙋 Author

Built by Misbah Sajjad as a hands-on project while learning AI & Data Science.