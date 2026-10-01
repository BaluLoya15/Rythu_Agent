from typing import Optional
from backend.models.schemas import RAGSearchResult
from backend.rag.retriever import get_agri_retriever

def search_agriculture_knowledge(query: str, crop: Optional[str] = None, optional_stage: Optional[str] = None, top_k: int = 3) -> RAGSearchResult:
    """
    RAG Tool wrapper that performs semantic and keyword TF-IDF retrieval
    over curated ANGRAU/ICAR agricultural extension documents.
    """
    search_query = query
    if optional_stage:
        search_query += f" stage {optional_stage}"
    
    retriever = get_agri_retriever()
    return retriever.search(query=search_query, crop=crop, top_k=top_k)
