import arxiv
from typing import List
from langchain_core.tools import tool
from tools.schemas import StandardPaper

@tool

def search_arxiv(query: str, max_results: int = 3) -> List[dict]:
    """
    Searches ArXiv for research papers based on a keyword query.
    Useful for finding the absolute latest pre-prints and technical methodologies.
    """

    try: 
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []

        for r in client.results(search):
            paper = StandardPaper(
                title=r.title,
                abstract=r.summary.replace("\n", " "),
                authors=[a.name for a in r.authors],
                year=r.published.year,
                url=r.pdf_url if r.pdf_url else r.entry_id,
                source="ArXiv",
                citation_count=0
            )
            results.append(paper.dump()) 
        
        return results
    
    except Exception as e:
        return [{"error": f"ArXiv search failed: {str(e)}"}]
    