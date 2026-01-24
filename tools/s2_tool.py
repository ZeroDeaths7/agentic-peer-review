import requests
import datetime
from typing import List
from langchain_core.tools import tool
from tools.schemas import StandardPaper

@tool
def search_semantic_scholar(query: str, max_results: int = 3) -> List[dict]:
    """
    Searches Semantic Scholar for published, peer-reviewed papers.
    Useful for finding influential papers ("Prior Art") and citation counts.
    """

    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"

        fields = "title, abstract,authors,year,url,citationCount" 
        
        params = {
            "query": query,
            "limit": max_results,
            "fields": fields
        }

        headers = {"User-Agent": "SocraticDebateAgent/1.0"}

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return [{"error": f"Semantic Scholar API error: {response.status_code} - {response.text}"}]
        
        data = response.json()

        if "data" not in data or not data["data"]:
            return [{"error": "No papers found for this query."}]
        
        results = []

        for r in data["data"]:
            authors = [author["name"] for author in r.get("authors", [])]
            paper = StandardPaper(
                title=r.get("title", "No Title"),
                abstract=r.get("abstract", "No Abstract").replace("\n", " "),
                authors=authors,
                year=r.get("year", datetime.datetime.now().year),
                url=r.get("url", "https://www.semanticscholar.org"),
                source="Semantic Scholar",
                citation_count=r.get("citationCount", 0)
            )

            results.append(paper.model_dump())

        return results
    
    
    except Exception as e:
        return [{"error": f"Semantic Scholar search failed: {str(e)}"}]