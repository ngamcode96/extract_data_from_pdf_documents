from dataclasses import dataclass, field
from typing import List, Dict
from .subclause import Subclause
from .node import Node

@dataclass
class Subtitle(Node):
    subtitle: str = "no_subtitle"
    text: str = ""
    subclauses: List[Subclause] = field(default_factory=list)
    definitions: Dict = field(default_factory=dict)
    page_number: int = 0

    def describe(self):
        result = self.subtitle if self.subtitle != "no_subtitle" else "" + "\n"
        result += self.text + "\n"
        result += "\n".join([subclause.describe() for subclause in self.subclauses])
        for key, values in self.definitions.items():
            result += key + "\n"
            result +=  "\n".join([definition.describe() for definition in values])
        return result
