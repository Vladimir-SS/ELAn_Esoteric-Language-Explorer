from typing import List, Dict
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

def get_esolang_from_query_result(esolang_name: str, result: List[Dict] ) -> Dict:
    print("Result: ", type(result))
    esolang = {
        "name": esolang_name,
        "url": None,
        "yearCreated": None,
        "shortDescription": None,
        "alias": None,
        "designedBy": None,
        "dimensions": set(),
        "memorySystem": set(),
        "paradigms": set(),
        "categories": set(),
        "influencedBy": set(),
        "influenced": set(),
        "fileExtensions": set(),
        "computationalClasses": set(),
        "typeSystems": set(),
        "dialects": set(),
    }

    for item in result:
        if not esolang["url"] and "url" in item:
            esolang["url"] = item["url"]["value"]
        if not esolang["yearCreated"] and "yearCreated" in item:
            esolang["yearCreated"] = item["yearCreated"]["value"]
        if not esolang["shortDescription"] and "shortDescription" in item:
            esolang["shortDescription"] = item["shortDescription"]["value"]
        if not esolang["alias"] and "alias" in item:
            esolang["alias"] = item["alias"]["value"]
        if not esolang["designedBy"] and "designedBy" in item:
            esolang["designedBy"] = item["designedBy"]["value"]
        if "memorySystem" in item:
            esolang["memorySystem"].add(item["memorySystem"]["value"])
        if "dimension" in item:
            esolang["dimensions"].add(item["dimension"]["value"])
        if "paradigm" in item:
            esolang["paradigms"].add(item["paradigm"]["value"])
        if "category" in item:
            esolang["categories"].add(item["category"]["value"])
        if "influencedBy" in item:
            esolang["influencedBy"].add(item["influencedBy"]["value"])
        if "influenced" in item:
            esolang["influenced"].add(item["influenced"]["value"])
        if "fileExtension" in item:
            esolang["fileExtensions"].add(item["fileExtension"]["value"])
        if "computationalClass" in item:
            esolang["computationalClasses"].add(item["computationalClass"]["value"])
        if "typeSystem" in item:
            esolang["typeSystems"].add(item["typeSystem"]["value"])
        if "dialect" in item:
            esolang["dialects"].add(item["dialect"]["value"])

    esolang["dimensions"] = list(esolang["dimensions"])
    esolang["memorySystem"] = list(esolang["memorySystem"])
    esolang["paradigms"] = list(esolang["paradigms"])
    esolang["categories"] = list(esolang["categories"])
    esolang["influencedBy"] = list(esolang["influencedBy"])
    esolang["influenced"] = list(esolang["influenced"])
    esolang["fileExtensions"] = list(esolang["fileExtensions"])
    esolang["computationalClasses"] = list(esolang["computationalClasses"])
    esolang["typeSystems"] = list(esolang["typeSystems"])
    esolang["dialects"] = list(esolang["dialects"])

    return esolang


def compute_embeddings(triples_result: List[Dict]) -> Dict:
    try:
        triples = [
            " ".join([binding["s"]["value"], binding["p"]["value"], binding["o"]["value"]])
            for binding in triples_result
        ]
        entities = list(set(binding["s"]["value"] for binding in triples_result))

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(triples)
        entity_embeddings = {}

        for entity in entities:
            entity_triples = [
                embedding
                for triple, embedding in zip(triples, embeddings)
                if entity in triple
            ]
            if entity_triples:
                entity_embeddings[entity] = np.mean(entity_triples, axis=0)

        with open("src/entity_embeddings.pkl", "wb") as f:
            pickle.dump(entity_embeddings, f)

        return entity_embeddings
    except Exception as e:
        raise e


def load_embeddings():
    try:
        with open("src/entity_embeddings.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
