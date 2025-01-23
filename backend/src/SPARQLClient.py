from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict

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