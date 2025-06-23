from dataclasses import dataclass, field
from typing import List
from .node import Node
from .subtitle import Subtitle

@dataclass
class Title(Node):
    title: str = "no_title"
    text: str = ""
    subtitles: List[Subtitle] = field(default_factory=list)
    page_number: int = 0

    def describe(self):
        result = self.title if self.title != "no_title" else "" + "\n"
        result += self.text + "\n"
        result += "\n".join([subtitle.describe() for subtitle in self.subtitles])
        return result

    @classmethod
    def seach_in_titles(cls, t, element):
        element = element.lower()
        return (element in t.title.lower() or element in t.text.lower())
