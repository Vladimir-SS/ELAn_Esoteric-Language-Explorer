import rdflib
import json
from urllib.parse import quote

graph = rdflib.Graph()
base_uri = "http://localhost:5173/esolangs/"
ESOLANG = rdflib.Namespace(base_uri)
OWL = rdflib.OWL
XSD = rdflib.XSD

graph.bind("esolang", ESOLANG)


def sanitize_uri(value):
    """
    Percent-encodes invalid characters in a URI fragment.
    """
    return quote(str(value).encode("utf-8"), safe="")


def add_uri_relation(graph, subject_uri, relationship_type_name, values, create_individuals=False):
    """
    Adds relationships to the graph, where both subject and object are URIs. Handles both single values and lists.
    """
    relationship_type = ESOLANG[relationship_type_name]
    if create_individuals:
        indiv_name = ESOLANG[relationship_type_name[3:]]  # Remove 'has' prefix

    if isinstance(values, list):
        for value in values:
            object_uri = ESOLANG[sanitize_uri(value)]
            if object_uri:
                graph.add((subject_uri, relationship_type, object_uri))
                create_individuals and create_individual(graph, indiv_name, object_uri)
    elif values:
        object_uri = ESOLANG[sanitize_uri(values)]
        if object_uri:
            graph.add((subject_uri, relationship_type, object_uri))
            create_individuals and create_individual(graph, indiv_name, object_uri)


def create_individual(graph, class_uri, individual_uri):
    graph.add((individual_uri, rdflib.RDF.type, class_uri))


with open("./data/esolangs-cleaned.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

for item in json_data:
    language_name = item["LanguageName"]
    sanitized_language_name = sanitize_uri(language_name)

    if sanitized_language_name is None:
        print(f"Skipping invalid language: {language_name}")
        continue

    language_uri = ESOLANG[sanitized_language_name]

    graph.add((language_uri, rdflib.RDF.type, ESOLANG.EsotericLanguage))

    if item.get("YearCreated"):
        graph.add((language_uri, ESOLANG.yearCreated, rdflib.Literal(item["YearCreated"], datatype=XSD.gYear)))

    if item.get("URL"):
        graph.add((language_uri, ESOLANG.url, rdflib.URIRef(item["URL"])))

    if item.get("DesignedBy"):
        graph.add((language_uri, ESOLANG.designedBy, rdflib.Literal(item["DesignedBy"], datatype=XSD.string)))

    if item.get("Alias"):
        graph.add((language_uri, ESOLANG.alias, rdflib.Literal(item["Alias"], datatype=XSD.string)))

    if item.get("InfluencedBy"):
        add_uri_relation(graph, language_uri, "influencedBy", item["InfluencedBy"])

    if item.get("Influenced"):
        add_uri_relation(graph, language_uri, "influenced", item["Influenced"])

    if item.get("ShortDescription"):
        graph.add((language_uri, ESOLANG.shortDescription, rdflib.Literal(item["ShortDescription"], datatype=XSD.string)))

    if item.get("Categories"):
        add_uri_relation(graph, language_uri, "hasCategory", item["Categories"], True)

    if item.get("Paradigms"):
        add_uri_relation(graph, language_uri, "hasParadigm", item["Paradigms"], True)

    if item.get("FileExtensions"):
        file_extensions = item["FileExtensions"] if isinstance(item["FileExtensions"], list) else []
        for extension in file_extensions:
            graph.add((language_uri, ESOLANG.fileExtension, rdflib.Literal(extension, datatype=XSD.string)))

output_file = "./data/esolangs-ontology.rdf"
graph.serialize(output_file, format="xml")
print(f"Ontology populated and saved as '{output_file}'")
