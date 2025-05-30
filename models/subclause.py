from dataclasses import dataclass, field
from typing import List, Dict
from .node import Node

@dataclass
class Subclause(Node):
    label: str = ""
    text: str = ""
    page_number: int = 0
    rank: int = 0

    def describe(self):
        return self.text