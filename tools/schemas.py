from pydantic import BaseModel, Field
from typing import List, Optional

class StandardPaper(BaseModel):
    """
    A unified schema for research papers, regardless of source (ArXiv vs S2).
    This ensures the 'Librarian' agent always sees the same data structure.
    """

    title: str = Field(description="The title of the research paper.")
    abstract: str = Field(description="The summary or abstract of the research paper.")
    authors: List[str] = Field(description="A list of author names.")
    year: int = Field(description="The publication year of the paper.")
    url: str = Field(description="A direct URL to access the paper or PDF.")
    source: str = Field(description="Source of the paper ('ArXiv' or 'Semantic Scholar').")
    citation_count: Optional[int] = Field(default=0, description="Number of times cited (proxy for impact).")

    def to_string(self) -> str:
        """Helper to format the paper for the LLM context window."""
        return (
            f"Title: {self.title}\n"
            f"Year: {self.year} | Citations: {self.citation_count} | Source: {self.source}\n"
            f"Authors: {', '.join(self.authors[:3])}\n"
            f"Abstract: {self.abstract}\n"
            f"Link: {self.url}\n"
            "---"
        )
    

    