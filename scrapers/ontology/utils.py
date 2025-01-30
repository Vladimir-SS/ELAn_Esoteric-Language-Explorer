import rdflib
from urllib.parse import quote

ESOLANG = rdflib.Namespace("http://localhost:5173/esolangs/")
OWL = rdflib.OWL
XSD = rdflib.XSD
RDFS = rdflib.RDFS
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")

def sanitize_uri(value):
    """
    Percent-encodes invalid characters in a URI fragment.
    """
    return quote(str(value).encode("utf-8"), safe="")

def add_relationships(graph, subject_uri, relationship_type_name, values, create_individuals=False):
    """
    Adds relationships to the graph, where both subject and object are URIs. Handles both single values and lists.
    """
    relationship_type = ESOLANG[relationship_type_name]
    if create_individuals:
        class_uri = ESOLANG[relationship_type_name[3:]]  # Remove 'has' prefix

    if isinstance(values, list):
        for value in values:
            object_uri = ESOLANG[sanitize_uri(value)]
            if object_uri:
                graph.add((subject_uri, relationship_type, object_uri))
                if create_individuals:
                    create_individual(graph, class_uri, object_uri)
    elif values:
        object_uri = ESOLANG[sanitize_uri(values)]
        if object_uri:
            graph.add((subject_uri, relationship_type, object_uri))
            if create_individuals:
                create_individual(graph, class_uri, object_uri)

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