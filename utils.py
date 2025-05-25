import re
from neo4j import GraphDatabase

def is_toc_page(page_text, min_toc_lines=3):
    toc_line_pattern = re.compile(r'.*\.{10,}\s*\d+')
    toc_lines = [line for line in page_text.split('\n') if toc_line_pattern.match(line)]
    if len(toc_lines) >= min_toc_lines:
        return True
    return False

def get_database_driver():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "")

    # Connect to Neo4j database
    driver = GraphDatabase.driver(URI, auth=AUTH)
    return driver