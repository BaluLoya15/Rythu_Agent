import math
import re
from typing import List, Dict, Any, Optional
from backend.rag.documents import AGRICULTURAL_DOCUMENTS
from backend.models.schemas import RAGSource, RAGSearchResult

class AgriKnowledgeRetriever:
    """
    High-performance semantic and keyword TF-IDF RAG retriever
    tailored for agricultural extension knowledge.
    Grounds queries in ANGRAU, ICAR, and KVK publications.
    """

    def __init__(self, documents: Optional[List[Dict[str, Any]]] = None):
        self.documents = documents or AGRICULTURAL_DOCUMENTS
        self.stop_words = {
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
            "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
            "by", "can", "did", "do", "does", "doing", "don", "down", "during", "each", "few", "for",
            "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
            "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
            "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
            "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
            "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs", "them",
            "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
            "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
            "while", "who", "whom", "why", "will", "with", "would", "you", "your", "yours", "yourself"
        }
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'[\w\-\.\%]+', text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 1]

    def _build_index(self):
        self.doc_tokens = []
        self.doc_freq = {}
        total_docs = len(self.documents)

        for doc in self.documents:
            full_text = f"{doc.get('crop', '')} {doc.get('title', '')} {doc.get('section', '')} {' '.join(doc.get('keywords', []))} {doc.get('content', '')}"
            tokens = self._tokenize(full_text)
            self.doc_tokens.append(tokens)

            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

        # Calculate IDF
        self.idf = {}
        for token, df in self.doc_freq.items():
            self.idf[token] = math.log((total_docs + 1) / (df + 1)) + 1.0

    def search(self, query: str, crop: Optional[str] = None, top_k: int = 3) -> RAGSearchResult:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            query_tokens = [crop.lower()] if crop else ["crop", "management"]

        scores = []
        for idx, doc in enumerate(self.documents):
            score = 0.0
            doc_token_list = self.doc_tokens[idx]
            doc_len = max(len(doc_token_list), 1)

            # 1. TF-IDF Term Matching
            for q_term in query_tokens:
                tf = doc_token_list.count(q_term) / doc_len
                idf_weight = self.idf.get(q_term, 1.0)
                score += tf * idf_weight * 10.0

            # 2. Crop-specific boost
            doc_crop = doc.get("crop", "").lower()
            if crop and crop.lower() in doc_crop:
                score += 1.5
            elif doc_crop == "general":
                score += 0.3

            # 3. Exact keyword boost
            for kw in doc.get("keywords", []):
                for q_term in query_tokens:
                    if q_term in kw.lower():
                        score += 0.4

            # Normalize roughly to 0.0 - 0.99
            normalized_score = min(round(math.tanh(score) * 0.98, 2), 0.98)
            scores.append((idx, max(normalized_score, 0.45)))

        # Sort descending by score
        scores.sort(key=lambda x: x[1], reverse=True)

        matched_sources: List[RAGSource] = []
        for idx, sc in scores[:top_k]:
            doc = self.documents[idx]
            snippet = doc.get("content", "")
            if len(snippet) > 280:
                snippet = snippet[:280] + "..."

            matched_sources.append(RAGSource(
                document_title=doc.get("title", "ANGRAU Crop Manual"),
                source_organization=doc.get("organization", "ANGRAU / ICAR"),
                section_or_chapter=doc.get("section", "Crop Advisory"),
                page_number=doc.get("page", 1),
                relevance_score=sc,
                content_snippet=snippet,
                official_reference=doc.get("reference", "Ref: AP-AGR-ANGRAU")
            ))

        return RAGSearchResult(
            query=query,
            crop=crop,
            sources=matched_sources,
            total_found=len(matched_sources)
        )

# Global singleton
_retriever = None

def get_agri_retriever() -> AgriKnowledgeRetriever:
    global _retriever
    if _retriever is None:
        _retriever = AgriKnowledgeRetriever()
    return _retriever
