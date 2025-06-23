from dataclasses import dataclass, field
from typing import List
from .node import Node
from .title import Title

@dataclass
class Doc(Node):
    file_path: str = ""
    total_pages: int = None
    titles: List[Title] = field(default_factory=list)

    def describe(self):
        result = "\n".join([title.describe() for title in self.titles])
        return result

    def get_titles(self):
        return self.titles
    
    def get_subtitles(self):
        subtitles = []
        for title in self.get_titles():
            subtitles += title.subtitles
        return subtitles
    
    def get_subclauses(self):
        subclauses = []
        for subtitle in self.get_subtitles():
            subclauses += subtitle.subclauses
        return subclauses

    def get_definitions(self):
        definitions = []
        for subtitle in self.get_subtitles():
            for term, values in subtitle.definitions.items():
                definitions += [{term: values}]
        return definitions
    
    def get_all_nodes(self):
        nodes = []
        nodes += self.get_titles()
        nodes += self.get_subtitles()
        nodes += self.get_subclauses()
        return nodes
