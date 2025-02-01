from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict, Any
import json

class SPARQLClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)

    def query(self, query: str) -> List[Dict]:
        """Executes a SPARQL query and returns the results as a list of dictionaries."""
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]

enpoint_url = "http://dbpedia.org/sparql"

sparql = SPARQLClient(enpoint_url)

query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?language ?shortDescription
                (COALESCE(?designer, ?developer) AS ?designedBy)
                ?paradigm ?memorySystem
                (COALESCE(?released, ?date) AS ?yearCreated)
                ?influencedBy ?influenced
                (COALESCE(?fileExt1, ?fileExt2) AS ?fileExtensions)
                ?languageName ?url
WHERE {
  ?language a dbo:ProgrammingLanguage ;
            dbo:abstract ?shortDescription ;
            dcterms:subject dbc:Esoteric_programming_languages .

  OPTIONAL { ?language dbp:paradigm ?paradigm. }
  OPTIONAL { ?language dbp:designer ?designer. }
  OPTIONAL { ?language dbp:developer ?developer. }
  OPTIONAL { ?language dbp:released ?released. }
  OPTIONAL { ?language dbp:date ?date. }
  OPTIONAL { ?language dbp:memorySystem ?memorySystem. }
  OPTIONAL { ?language dbp:implementations ?referenceImplementation. }
  OPTIONAL { ?language dbp:influencedBy ?influencedBy. }
  OPTIONAL { ?language dbp:influenced ?influenced. }
  OPTIONAL { ?language dbp:fileExtensions ?fileExt1. }
  OPTIONAL { ?language dbp:fileExt ?fileExt2. }
  OPTIONAL { ?language rdfs:label ?languageName. }
  OPTIONAL { ?language dbp:url ?url. }

  FILTER (lang(?shortDescription) = "en")  # Filters abstracts in English
}
"""

results = sparql.query(query)

def transform_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms a SPARQL result into a structured dictionary."""
    def get_value(key):
        return result[key]["value"] if key in result else None

    file_extensions = get_value("fileExtensions")
    if file_extensions:
        file_extensions = file_extensions.split(", ")

    paradigms = get_value("paradigm")
    if paradigms:
        paradigms = paradigms.split(", ")
        print(paradigms)

    return {
        "Paradigms": paradigms,
        "DesignedBy": get_value("designedBy"),
        "YearCreated": get_value("yearCreated"),
        "MemorySystem": get_value("memorySystem"),
        "InfluencedBy": get_value("influencedBy"),
        "Influenced": get_value("influenced"),
        "FileExtensions": file_extensions,
        "LanguageName": get_value("languageName"),
        "URL": get_value("url"),
        "ShortDescription": get_value("shortDescription"),
        "Source": get_value("language")
    }

def update_existing_data(existing_entry: Dict[str, Any], new_entry: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in new_entry.items():
        if value:
            existing_entry[key] = value
    return existing_entry

new_data = [transform_result(result) for result in results]

input_file = "data/esolangs-data.json"
output_file = "data/esolangs-data-with-dbpedia.json"

try:
    with open(input_file, "r", encoding="utf-8") as file:
        existing_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    existing_data = []

existing_languages = {entry["LanguageName"]: entry for entry in existing_data}

for new_entry in new_data:
    lang_name = new_entry["LanguageName"]
    if lang_name in existing_languages:
        existing_languages[lang_name] = update_existing_data(existing_languages[lang_name], new_entry)
    else:
        existing_data.append(new_entry)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(list(existing_languages.values()), file, indent=4, ensure_ascii=False)