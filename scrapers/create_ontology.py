import rdflib
import json
from urllib.parse import quote

g = rdflib.Graph()
base_uri = "http://localhost:5173/esolangs/"
ESOLANG = rdflib.Namespace(base_uri)
OWL = rdflib.OWL
XSD = rdflib.XSD

g.bind("esolang", ESOLANG)

def sanitize_uri(value):
    """
    Percent-encodes invalid characters in a URI fragment.
    """
    return quote(str(value).encode('utf-8'), safe="")

def create_individual(graph, class_uri, individual_uri):
    graph.add((individual_uri, rdflib.RDF.type, class_uri))

with open("./data/esolangs-cleaned.json", 'r', encoding='utf-8') as f:
    json_data = json.load(f)

for item in json_data:
    language_name = item["LanguageName"]
    sanitized_language_name = sanitize_uri(language_name)

    if sanitized_language_name is None:
        print(f"Skipping invalid language: {language_name}")
        continue

    language_uri = ESOLANG[sanitized_language_name]

    g.add((language_uri, rdflib.RDF.type, ESOLANG.EsotericLanguage))

    if item.get("YearCreated"):
        g.add((language_uri, ESOLANG.yearCreated, rdflib.Literal(item["YearCreated"], datatype=XSD.gYear)))

    if item.get("URL"):
        g.add((language_uri, ESOLANG.url, rdflib.URIRef(item["URL"])))

    if item.get("DesignedBy"):
        g.add((language_uri, ESOLANG.designedBy, rdflib.Literal(item["DesignedBy"], datatype=XSD.string)))

    if item.get("Alias"):
        g.add((language_uri, ESOLANG.alias, rdflib.Literal(item["Alias"], datatype=XSD.string)))

    if item.get("InfluencedBy"):
            influenced_by = item["InfluencedBy"] if isinstance(item["InfluencedBy"], list) else []
            for influenced in influenced_by:
                influenced_uri = ESOLANG[sanitize_uri(influenced)]
                if influenced_uri:
                    g.add((language_uri, ESOLANG.influencedBy, influenced_uri))

    if item.get("Influenced"):
        influenced = item["Influenced"] if isinstance(item["Influenced"], list) else []
        for influence in influenced:
            influence_uri = ESOLANG[sanitize_uri(influence)]
            if influence_uri:
                g.add((language_uri, ESOLANG.influenced, influence_uri))

    if item.get("ShortDescription"):
        g.add((language_uri, ESOLANG.shortDescription, rdflib.Literal(item["ShortDescription"], datatype=XSD.string)))

    if item.get("Categories"):
        for category in item["Categories"]:
            category_uri = ESOLANG[sanitize_uri(category)]
            if category_uri:
                g.add((language_uri, ESOLANG.hasCategory, category_uri))
                create_individual(g, ESOLANG.Category, category_uri)

    if item.get("Paradigms"):
        paradigms = item["Paradigms"].split(";") if isinstance(item["Paradigms"], str) else []
        for paradigm in paradigms:
            paradigm_uri = ESOLANG[paradigm.strip()]
            if paradigm_uri:
                g.add((language_uri, ESOLANG.hasParadigm, paradigm_uri))
                create_individual(g, ESOLANG.Paradigm, paradigm_uri)

    if item.get("FileExtensions"):
        file_extensions = item["FileExtensions"] if isinstance(item["FileExtensions"], list) else []
        for extension in file_extensions:
            g.add((language_uri, ESOLANG.fileExtension, rdflib.Literal(extension, datatype=XSD.string)))

output_file = "./data/esolangs-ontology.rdf"
g.serialize(output_file, format="xml")
print(f"Ontology populated and saved as '{output_file}'")