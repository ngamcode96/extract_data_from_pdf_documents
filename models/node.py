from dataclasses import dataclass, fields
from typing import List

@dataclass
class Node:
    id: str = ""
    label: str = ""

    @classmethod
    def from_node(cls, node):
        """Create a dataclass instance from a Neo4j node with filtering."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in node.items() if k in valid_fields}
        return cls(**filtered_data)