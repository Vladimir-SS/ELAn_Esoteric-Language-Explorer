from typing import List, Optional
BASE_URI = "https://frontend-728286732053.us-central1.run.app/esolangs/"

PREFIXES = f"""
PREFIX esolang: <{BASE_URI}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

ESOLANGS_NAME_LIST_QUERY = PREFIXES + f"""
SELECT (STRAFTER(STR(?esolang), "{BASE_URI}") AS ?name)
WHERE {{
  ?esolang rdf:type esolang:EsotericLanguage .
}}
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
        FILTER (STRAFTER(STR(?esolang), "{BASE_URI}") = "{esolang_name}")
        """
    query += "}"

    return query


def create_filter_query_parts(property_name: str, property_path: str, values: List[str]) -> str:
    query_parts = []
    if values:
        for value in values:
            query_parts.append(f"?esolang esolang:{property_name} <{BASE_URI}{property_path}/{value}> .")

    return query_parts


def create_esolang_search_query(
    search_term: str,
    year_created: List[str],
    paradigm: List[str],
    category: List[str],
    memory_system: List[str],
    dimension: List[str],
    computational_class: List[str],
    file_extension: List[str],
    type_system: List[str],
    dialect: List[str],
    limit: Optional[int],
    offset: Optional[int]
) -> str:
    query_parts = [
        f'SELECT (STRAFTER(STR(?esolang), "{BASE_URI}") AS ?name) WHERE {{',
        "?esolang rdf:type esolang:EsotericLanguage .",
    ]

    if search_term:
        query_parts.append(f"FILTER(CONTAINS(LCASE(STR(?esolang)), LCASE('{search_term}')))")

    if paradigm:
        query_parts.extend(create_filter_query_parts("hasParadigm", "paradigm", paradigm))

    if category:
        query_parts.extend(create_filter_query_parts("hasCategory", "category", category))

    if memory_system:
        query_parts.extend(create_filter_query_parts("hasMemorySystem", "memory-system", memory_system))

    if dimension:
        query_parts.extend(create_filter_query_parts("hasDimension", "dimension", dimension))

    if computational_class:
        query_parts.extend(create_filter_query_parts("hasComputationalClass", "computational-class", computational_class))

    if type_system:
        query_parts.extend(create_filter_query_parts("hasTypeSystem", "type-system", type_system))

    if dialect:
        query_parts.extend(create_filter_query_parts("hasDialect", "dialect", dialect))

    if file_extension:
        for value in file_extension:
            query_parts.append(f"?esolang esolang:fileExtension \"{value}\" .")

    if year_created:
        query_parts.insert(0, "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>")
        query_parts.append("?esolang esolang:yearCreated ?yearCreated .")
        years_values = " ".join([f'"{year}"^^xsd:gYear' for year in year_created])
        query_parts.append(f"VALUES ?yearCreated {{{years_values}}}")

    query_parts.append("}")

    if limit is not None:
        query_parts.append(f"LIMIT {limit}")
    if offset is not None:
        query_parts.append(f"OFFSET {offset}")

    return PREFIXES + "\n".join(query_parts)


def create_years_created_query() -> str:
    query = (
        PREFIXES
        + """
        SELECT DISTINCT ?yearCreated
        WHERE {
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:yearCreated ?yearCreated .
        }
        ORDER BY ?yearCreated
        """
    )

    return query


def create_categories_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?category), "{BASE_URI}category/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasCategory ?category .
        }}
        ORDER BY ?category
        """
    )

    return query


def create_paradigms_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?paradigm), "{BASE_URI}paradigm/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasParadigm ?paradigm .
        }}
        ORDER BY ?paradigm
        """
    )

    return query


def create_computational_classes_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?computationalClass), "{BASE_URI}computational-class/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasComputationalClass ?computationalClass .
        }}
        ORDER BY ?computationalClass
        """
    )

    return query


def create_memory_systems_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?memorySystem), "{BASE_URI}memory-system/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasMemorySystem ?memorySystem .
        }}
        ORDER BY ?memorySystem
        """
    )

    return query


def create_dimensions_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?dimension), "{BASE_URI}dimension/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasDimension ?dimension .
        }}
        ORDER BY ?dimension
        """
    )

    return query


def create_type_systems_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?typeSystem), "{BASE_URI}type-system/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasTypeSystem ?typeSystem .
        }}
        ORDER BY ?typeSystem
        """
    )

    return query


def create_dialects_query() -> str:
    query = (
        PREFIXES
        + f"""
        SELECT DISTINCT (STRAFTER(STR(?dialect), "{BASE_URI}dialect/") AS ?name)
        WHERE {{
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:hasDialect ?dialect .
        }}
        ORDER BY ?dialect
        """
    )

    return query


def create_file_extensions_query() -> str:
    query = (
        PREFIXES
        + """
        SELECT DISTINCT ?fileExtension
        WHERE {
          ?esolang rdf:type esolang:EsotericLanguage .
          ?esolang esolang:fileExtension ?fileExtension .
        }
        ORDER BY ?fileExtension
        """
    )

    return query

def create_all_triples_query() -> str:
    query = (
        PREFIXES
        + """
        SELECT ?s ?p ?o
        WHERE {
          ?s ?p ?o
        }
        """
    )

    return query