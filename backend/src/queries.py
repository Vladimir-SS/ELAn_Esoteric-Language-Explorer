PREFIXES = """
PREFIX esolang: <http://localhost:5173/esolangs/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

ESOLANGS_NAME_LIST_QUERY = PREFIXES + """
SELECT (STRAFTER(STR(?esolang), "http://localhost:5173/esolangs/") AS ?name)
WHERE {
  ?esolang rdf:type esolang:EsotericLanguage .
}
"""

def create_esolang_name_query(esolang_name: str | None) -> str:
    query = (
        PREFIXES
        + """
      SELECT ?esolang ?yearCreated ?url ?shortDescription ?alias ?designedBy ?paradigm ?influencedBy ?influenced ?category ?fileExtension ?computationalClass ?typeSystem ?dialect ?dimension ?memorySystem
      WHERE {
        ?esolang rdf:type esolang:EsotericLanguage .
        ?esolang esolang:url ?url .
        OPTIONAL { ?esolang esolang:yearCreated ?yearCreated . }
        OPTIONAL { ?esolang esolang:shortDescription ?shortDescription . }
        OPTIONAL { ?esolang esolang:alias ?alias . }
        OPTIONAL { ?esolang esolang:designedBy ?designedBy . }
        OPTIONAL { ?esolang esolang:hasParadigm ?paradigm . }
        OPTIONAL { ?esolang esolang:influencedBy ?influencedBy . }
        OPTIONAL { ?esolang esolang:influenced ?influenced . }
        OPTIONAL { ?esolang esolang:hasCategory ?category . }
        OPTIONAL { ?esolang esolang:fileExtension ?fileExtension . }
        OPTIONAL { ?esolang esolang:hasComputationalClass ?computationalClass . }
        OPTIONAL { ?esolang esolang:hasTypeSystem ?typeSystem . }
        OPTIONAL { ?esolang esolang:hasDialect ?dialect . }
        OPTIONAL { ?esolang esolang:hasDimension ?dimension . }
        OPTIONAL { ?esolang esolang:hasMemorySystem ?memorySystem . }
      """
    )

    if esolang_name:
        query += f"""
        FILTER (STRAFTER(STR(?esolang), "http://localhost:5173/esolangs/") = "{esolang_name}")
        """
    query += "}"

    return query


def create_esolang_search_query(search_term: str, limit: int, offset: int) -> str:
    safe_search_term = search_term.replace('"', '\\"')

    query = (
        PREFIXES
        + f"""
        SELECT ?esolang
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          FILTER (CONTAINS(LCASE(STRAFTER(STR(?esolang), "http://localhost:5173/esolangs/")), LCASE("{safe_search_term}")))
        }}
        LIMIT {limit} OFFSET {offset}
        """
    )

    return query
