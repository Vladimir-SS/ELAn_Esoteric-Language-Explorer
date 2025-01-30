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


def add_relationships(graph, subject_uri, relationship_type_name, values, create_individuals=False):
    """
    Adds semantic relationships between a specified subject and one or more object URIs in an RDF graph.
    Optionally creates individual entities for each object URI.
    """
    relationship_type = ESOLANG[relationship_type_name]
    if create_individuals:
        class_uri = ESOLANG[relationship_type_name[3:]]  # Remove 'has' prefix

    if isinstance(values, list):
        for value in values:
            object_uri = ESOLANG[sanitize_uri(value)]
            if object_uri:
                graph.add((subject_uri, relationship_type, object_uri))
                create_individuals and create_individual(graph, class_uri, object_uri)
    elif values:
        object_uri = ESOLANG[sanitize_uri(values)]
        if object_uri:
            graph.add((subject_uri, relationship_type, object_uri))
            create_individuals and create_individual(graph, class_uri, object_uri)


def create_individual(graph, class_uri, individual_uri):
    graph.add((individual_uri, rdflib.RDF.type, class_uri))


def define_subcategories(graph):
    category_uri = ESOLANG["Category"]
    computational_class_uri = ESOLANG["ComputationalClass"]
    memory_system_uri = ESOLANG["MemorySystem"]
    dimension_uri = ESOLANG["Dimension"]
    paradigm_uri = ESOLANG["Paradigm"]

    # Define each as a subclass of Category
    graph.add((computational_class_uri, rdflib.RDFS.subClassOf, category_uri))
    graph.add((memory_system_uri, rdflib.RDFS.subClassOf, category_uri))
    graph.add((dimension_uri, rdflib.RDFS.subClassOf, category_uri))
    graph.add((paradigm_uri, rdflib.RDFS.subClassOf, category_uri))


def is_instance_of_subcategory(graph, category_uri, superclass_uri):
    """
    Check if category_uri is an instance of any subclass of superclass_uri.
    """
    query = """
    ASK WHERE {
        ?category_uri rdf:type ?subclass .
        ?subclass rdfs:subClassOf* ?superclass_uri .
    }
    """

    result = graph.query(query, initBindings={"category_uri": category_uri, "superclass_uri": superclass_uri})

    return bool(result)

with open("./data/esolangs-cleaned.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

define_subcategories(graph)

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
        general_categories = [category for category in item["Categories"] if not is_instance_of_subcategory(graph, ESOLANG[sanitize_uri(category)], ESOLANG.Category)]
        add_relationships(graph, language_uri, "hasCategory", general_categories, True)

    if item.get("FileExtensions"):
        file_extensions = item["FileExtensions"] if isinstance(item["FileExtensions"], list) else []
        for extension in file_extensions:
            graph.add((language_uri, ESOLANG.fileExtension, rdflib.Literal(extension, datatype=XSD.string)))

output_file = "./data/esolangs-ontology.rdf"
graph.serialize(output_file, format="xml")
print(f"Ontology populated and saved as '{output_file}'")
