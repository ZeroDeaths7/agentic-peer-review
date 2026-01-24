import requests
import datetime
import time
from typing import List
from langchain_core.tools import tool
from tools.schemas import StandardPaper

# Import retry logic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Define a custom exception for Rate Limits so we can retry specifically on them
class RateLimitError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3),              # Try 3 times max
    wait=wait_exponential(multiplier=2, min=2, max=10), # Wait 2s, 4s, 8s
    retry=retry_if_exception_type(RateLimitError) # Only retry on 429 errors
)
def fetch_from_s2(url, params, headers):
    response = requests.get(url, params=params, headers=headers, timeout=10)
    if response.status_code == 429:
        print("⚠️ Rate limit hit (429). Retrying...")
        raise RateLimitError("Rate limit hit")
    return response

@tool
def search_semantic_scholar(query: str, max_results: int = 3) -> List[dict]:
    """
    Searches Semantic Scholar with automatic retry logic for rate limits.
    """
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        fields = "title,abstract,authors,year,url,citationCount"
        params = {"query": query, "limit": max_results, "fields": fields}
        headers = {"User-Agent": "SocraticDebateBot/1.0"}

        # Call the helper function with retry logic
        response = fetch_from_s2(url, params, headers)
        
        if response.status_code != 200:
            return [{"error": f"API Error: {response.status_code}"}]
            
        data = response.json()
        if "data" not in data or not data["data"]:
            return [{"message": "No papers found."}]

        results = []
        for item in data["data"]:
            authors = [a["name"] for a in item.get("authors", [])]
            paper = StandardPaper(
                title=item.get("title", "Unknown"),
                abstract=item.get("abstract", "No abstract."),
                authors=authors,
                year=item.get("year", 0),
                url=item.get("url", ""),
                source="Semantic Scholar",
                citation_count=item.get("citationCount", 0)
            )
            results.append(paper.model_dump())
            
        return results

    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]