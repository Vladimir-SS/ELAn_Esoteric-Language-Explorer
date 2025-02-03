import rdflib
from urllib.parse import quote

ESOLANG = rdflib.Namespace("https://frontend-728286732053.us-central1.run.app/esolangs/")
OWL = rdflib.OWL
XSD = rdflib.XSD
RDFS = rdflib.RDFS
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")

uri_prefixes = {
    "hasParadigm": "paradigm",
    "hasComputationalClass": "computational-class",
    "hasMemorySystem": "memory-system",
    "hasDimension": "dimension",
    "hasCategory": "category",
    "hasTypeSystem": "type-system",
    "hasDialect": "dialect",
}

def sanitize_uri(value):
    """
    Percent-encodes invalid characters in a URI fragment.
    """
    return quote(str(value).encode("utf-8"), safe="")

def add_link(graph, subject_uri, relationship_type, prefix, value, class_uri=None):
    """
    Adds a relationship link to the graph with a properly formatted URI.
    """
    sanitized_value = sanitize_uri(value)
    if sanitized_value:
        object_uri = rdflib.URIRef(f"{ESOLANG}{prefix}{sanitized_value}")
        graph.add((subject_uri, relationship_type, object_uri))
        if class_uri:
            create_individual(graph, class_uri, object_uri)

def add_relationships(graph, subject_uri, relationship_type_name, values, create_individuals=False):
    """
    Adds relationships to the graph, where both subject and object are URIs. Handles both single values and lists.
    """
    relationship_type = ESOLANG[relationship_type_name]

    class_uri = ESOLANG[relationship_type_name[3:]] if create_individuals else None

    prefix = uri_prefixes.get(relationship_type_name, "")
    if prefix:
        prefix += "/"

    if isinstance(values, list):
        for value in values:
            add_link(graph, subject_uri, relationship_type, prefix, value, class_uri)
    elif values:
        add_link(graph, subject_uri, relationship_type, prefix, values, class_uri)

def create_individual(graph, class_uri, individual_uri):
    graph.add((individual_uri, rdflib.RDF.type, class_uri))

def add_property_metadata(graph, property_uri, label, comment, domain, range):
    """
    Add metadata (rdfs:label, rdfs:comment, rdfs:domain, rdfs:range) for a given property.
    """
    graph.add((property_uri, rdflib.RDF.type, rdflib.RDF.Property))
    graph.add((property_uri, RDFS.label, rdflib.Literal(label, lang="en")))
    graph.add((property_uri, RDFS.comment, rdflib.Literal(comment, lang="en")))
    graph.add((property_uri, RDFS.domain, domain))
    graph.add((property_uri, RDFS.range, range))

def create_sub_class_of(graph, subclass_uri, superclass_uri):
    """
    Add a subclass relationship between two classes.
    """
    graph.add((subclass_uri, RDFS.subClassOf, superclass_uri))