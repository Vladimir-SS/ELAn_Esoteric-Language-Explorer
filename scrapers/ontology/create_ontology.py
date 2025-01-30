import rdflib
import json
from utils import (
    sanitize_uri, add_relationships, create_individual,
    add_property_metadata, create_sub_class_of
)

graph = rdflib.Graph()
base_uri = "http://localhost:5173/esolangs/"

OWL = rdflib.OWL
XSD = rdflib.XSD
ESOLANG = rdflib.Namespace(base_uri)
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")

graph.bind("esolang", ESOLANG)

subcategories = [
    ESOLANG["ComputationalClass"],
    ESOLANG["MemorySystem"],
    ESOLANG["Dimension"],
    ESOLANG["Paradigm"],
]

def is_subcategory(category_uri):
    return category_uri in subcategories

with open("./data/esolangs-cleaned.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

for subcategory in subcategories:
    create_sub_class_of(graph, subcategory, ESOLANG.Category)

add_property_metadata(graph, ESOLANG.url, "url",
                      "Links to the official URL of the esolang.",
                      ESOLANG.EsotericLanguage, XSD.anyURI)

add_property_metadata(graph, ESOLANG.designedBy, "designedBy",
                      "Indicates the person who designed an esolang.",
                      ESOLANG.EsotericLanguage, FOAF.Person)

add_property_metadata(graph, ESOLANG.shortDescription, "shortDescription",
                      "A brief description of the esolang.",
                      ESOLANG.EsotericLanguage, XSD.string)

add_property_metadata(graph, ESOLANG.influencedBy, "influencedBy",
                        "Indicates the esoteric languages that influenced an esolang.",
                        ESOLANG.EsotericLanguage, ESOLANG.EsotericLanguage)

add_property_metadata(graph, ESOLANG.hasCategory, "hasCategory",
                      "Links an esolang to its category.",
                      ESOLANG.EsotericLanguage, ESOLANG.Category)

add_property_metadata(graph, ESOLANG.hasParadigm, "hasParadigm",
                      "Links an esolang to its programming paradigm.",
                      ESOLANG.EsotericLanguage, ESOLANG.Paradigm)

graph.add((ESOLANG.influenced, OWL.inverseOf, ESOLANG.influencedBy))

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

    if item.get("ShortDescription"):
        graph.add((language_uri, ESOLANG.shortDescription, rdflib.Literal(item["ShortDescription"], datatype=XSD.string)))

    if item.get("InfluencedBy"):
        add_relationships(graph, language_uri, "influencedBy", item["InfluencedBy"])

    if item.get("Influenced"):
        add_relationships(graph, language_uri, "influenced", item["Influenced"])

    if item.get("Dialects"):
        add_relationships(graph, language_uri, "hasDialect", item["Dialects"], True)

    if item.get("TypeSystem"):
        add_relationships(graph, language_uri, "hasTypeSystem", item["TypeSystem"], True)

    if item.get("Paradigms"):
        add_relationships(graph, language_uri, "hasParadigm", item["Paradigms"], True)

    if item.get("ComputationalClass"):
        add_relationships(graph, language_uri, "hasComputationalClass", item["ComputationalClass"], True)

    if item.get("MemorySystem"):
        add_relationships(graph, language_uri, "hasMemorySystem", item["MemorySystem"], True)

    if item.get("Dimensions"):
        add_relationships(graph, language_uri, "hasDimension", item["Dimensions"], True)

    if item.get("Categories"):
        general_categories = [category for category in item["Categories"] if not is_subcategory(ESOLANG[sanitize_uri(category)])]
        add_relationships(graph, language_uri, "hasCategory", general_categories, True)

    if item.get("FileExtensions"):
        file_extensions = item["FileExtensions"] if isinstance(item["FileExtensions"], list) else []
        for extension in file_extensions:
            graph.add((language_uri, ESOLANG.fileExtension, rdflib.Literal(extension, datatype=XSD.string)))

output_file = "./data/esolangs-ontology.rdf"
graph.serialize(output_file, format="xml")
print(f"Ontology populated and saved as '{output_file}'")
