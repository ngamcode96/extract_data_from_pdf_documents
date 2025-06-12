import os
import re
from neo4j import GraphDatabase
from dotenv import load_dotenv
import yaml
from llm import llm_response
from models.title import Title
import json


load_dotenv()
def is_toc_page(page_text, min_toc_lines=3):
    toc_line_pattern = re.compile(r"(SCHEDULE\s*)?(\d+\.?)\s*([\w+\s*]+)\s*(\.{4,})\s*\d+")
    toc_lines = [line for line in page_text.split('\n') if toc_line_pattern.match(line)]
    if len(toc_lines) >= min_toc_lines:
        return True
    return False

def extract_titles_from_toc(pages):
    toc_line_pattern = re.compile(r"(SCHEDULE\s*)?(\d+\.?)\s*([\w+\s*]+)\s*(\.{4,})\s*\d+")
    titles = []
    for page in pages:
       text = page.get('text')
       lines = text.split('\n')
       for line in lines:
           match_line = toc_line_pattern.match(line)
           if match_line:
               title = str(match_line.group(3)).lower()
               titles.append(title)
    return titles

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


def search_by_title(title):
    driver = get_database_driver()
    query = f"""
        MATCH (start:Title)
        WHERE toLower(start.title) CONTAINS "{title.lower()}"
        CALL apoc.path.spanningTree(
        start,
        {{
            relationshipFilter: "HAS_SUBTITLE>|HAS_SUBCLAUSE>|HAS_DEFINITION>",
            labelFilter: "+Subtitle|+Subclause|+Definition",
            maxLevel: 10
        }}
        )
        YIELD path
        WITH path, nodes(path) AS nds
        UNWIND nds AS node
        RETURN DISTINCT node
        ORDER BY
        coalesce(node.page_number, 0) ASC,
        coalesce(node.rank, "") ASC
    """
    result = driver.execute_query(query)
    titles = [Title.from_node(record["node"]) for record in result.records]
    text = ""
    for t in titles:
        text += t.describe()
    return text

def extract_datapoint(datapoint, context_from=None):
    context = ""
    structured_output = None
    if not context_from:
        for title in datapoint["search"]["titles"]:
            context += search_by_title(title)
    else:
        context = context_from
    prompt = datapoint.get("prompt")
    if prompt:
        filled_prompt = prompt.replace("{{context}}", context)
        structured_output = llm_response(filled_prompt)

    custom_output = datapoint.get("custom_output")
    if custom_output:
        boolean_check = custom_output.get('bool')
        if boolean_check:
            key = boolean_check.get("key")
            ctx = boolean_check.get("context")
            if ctx == "empty":
                structured_output = {key: len(context) > 0}

    try:
        structured_output = json.loads(structured_output)
    except Exception as e:
        print("error parsing:", e)
    return {"structured_output": structured_output, "context": context}