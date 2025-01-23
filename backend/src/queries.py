PREFIXES = """
PREFIX esolang: <https://no-domain.sadly/ontology/esoteric_languages#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

ESOLANG_NAME_QUERY = PREFIXES + """
SELECT (STRAFTER(STR(?esolang), "#") AS ?name)
WHERE {
  ?esolang rdf:type esolang:EsotericLanguage .
}
"""

ESOLANG_QUERY = PREFIXES + """
SELECT ?esolang ?yearCreated ?url ?shortDescription
WHERE {
  ?esolang rdf:type esolang:EsotericLanguage .
  ?esolang esolang:yearCreated ?yearCreated .
  ?esolang esolang:url ?url .
  ?esolang esolang:shortDescription ?shortDescription .
}
"""