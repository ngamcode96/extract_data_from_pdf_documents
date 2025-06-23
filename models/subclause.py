from dataclasses import dataclass, field
from typing import List, Dict
from .node import Node
from bm25 import search_bm25
from embedding import compute_similarity
@dataclass
class Subclause(Node):
    label: str = ""
    text: str = ""
    page_number: int = 0
    rank: int = 0

    def describe(self):
        return self.text

    @classmethod
    def search_definition(cls, d, element):
        if element in d:
            return True
        return False
    
    @classmethod
    def search_subclause(cls, sc, element):
        if element in sc.text:
            return True
        return False
    
    @classmethod
    def fulltext_search(cls, query, subclauses, top_n=3):
        docs = [subclause.text for subclause in subclauses]
        result = search_bm25(docs, query, top_n=top_n)
        return result
    
    @classmethod
    def similarity_search(cls, query, subclauses, top_k=3):
        docs = [doc.text for doc in subclauses]
        scores, best_idx = compute_similarity(docs, query, top_k=top_k)
        result = [(subclauses[idx], scores[idx]) for idx in best_idx]
        return result