from dataclasses import dataclass, fields, field
from typing import List
from models.bbox import Bbox
from models.cell import Cell
from bm25 import search_bm25
@dataclass
class Node:
    id: str = ""
    label: str = ""
    bboxes: List[Bbox] = field(default_factory=list)
    cells: List[Cell] = field(default_factory=list)

    @classmethod
    def from_node(cls, node):
        """Create a dataclass instance from a Neo4j node with filtering."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in node.items() if k in valid_fields}
        return cls(**filtered_data)

    def print_node(self):
        print(self.describe())

    @classmethod
    def global_search(cls, query, data, top_n=3):
        docs = [node.describe() for node in data if isinstance(node, Node)]
        docs = [node for node in docs if node is not None]
        result = search_bm25(docs, query, top_n=top_n)
        return result

    def search(self, map_function, data):
        mapped = map(lambda x: map_function(x), data)
        return [item for item, match in zip(data, mapped) if match]