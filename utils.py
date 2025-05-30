import os
import re
from neo4j import GraphDatabase
from dotenv import load_dotenv
import yaml

load_dotenv()
def is_toc_page(page_text, min_toc_lines=3):
    toc_line_pattern = re.compile(r'.*\.{10,}\s*\d+')
    toc_lines = [line for line in page_text.split('\n') if toc_line_pattern.match(line)]
    if len(toc_lines) >= min_toc_lines:
        return True
    return False

def get_database_driver():
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    # Connect to Neo4j database
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return driver

def load_yaml_file(file_path):
    with open(file_path, "r") as f:
        content = yaml.safe_load(f)
    return content