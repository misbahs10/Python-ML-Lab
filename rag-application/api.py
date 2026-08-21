import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI
from pydantic import BaseModel
from qa_chain import ask_question #type: ignore

app = FastAPI(title="RAG Application API")


class QueryRequest(BaseModel):
    question: str
    k: int = 3


class SourceInfo(BaseModel):
    source: str
    page: int


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceInfo]


@app.get("/")
def root():
    return {"message": "RAG Application API is running ✅"}


@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):
    answer, sources = ask_question(request.question, k=request.k)

    source_list = [
        SourceInfo(
            source=doc.metadata.get("source", "unknown"),
            page=doc.metadata.get("page", -1)
        )
        for doc in sources
    ]

    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=source_list
    )