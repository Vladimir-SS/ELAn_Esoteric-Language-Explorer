from typing import List, Dict

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
