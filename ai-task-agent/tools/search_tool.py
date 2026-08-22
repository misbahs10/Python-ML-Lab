# tools/search_tool.py
import os
from tavily import TavilyClient #type: ignore

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    """Web se current info fetch karta hai."""
    results = tavily.search(query=query, max_results=3)
    return str(results["results"])