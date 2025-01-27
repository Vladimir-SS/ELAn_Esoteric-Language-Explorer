from typing import List, Dict
from fastapi import FastAPI, HTTPException
from src import SPARQLClient
from src import ESOLANGS_NAME_LIST_QUERY, create_esolang_name_query

app = FastAPI()

sparql_client = SPARQLClient("http://host.docker.internal:3030/Esolangs/sparql") # Change to "http://localhost:3030/Esolangs/sparql" if not using Docker

@app.get("/api/esolangs", response_model=List[str])
def get_esolangs():
    """Fetch all esolangs from the SPARQL endpoint."""
    try:
        result = sparql_client.query(ESOLANGS_NAME_LIST_QUERY)
        if not result:
            raise HTTPException(status_code=404, detail="No esolangs found.")
        esolangs = [esolang["name"]["value"] for esolang in result]
        return esolangs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/esolangs/{esolang_name}", response_model=Dict)
async def get_esolang(esolang_name: str):
    """Fetch details of a specific esolang from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_esolang_name_query(esolang_name))
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")

        esolang = {
            "name": esolang_name,
            "url": None,
            "yearCreated": None,
            "shortDescription": None,
            "alias": None,
            "designedBy": None,
            "categories": set(),
            "influencedBy": set(),
            "influenced": set(),
            "fileExtensions": set()
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

            if "category" in item:
                esolang["categories"].add(item["category"]["value"])
            if "influencedBy" in item:
                esolang["influencedBy"].add(item["influencedBy"]["value"])
            if "influenced" in item:
                esolang["influenced"].add(item["influenced"]["value"])
            if "fileExtensions" in item:
                esolang["fileExtensions"].add(item["fileExtensions"]["value"])

        esolang["categories"] = list(esolang["categories"])
        esolang["influencedBy"] = list(esolang["influencedBy"])
        esolang["influenced"] = list(esolang["influenced"])
        esolang["fileExtensions"] = list(esolang["fileExtensions"])

        return esolang

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sparsql-data", response_model=List[dict])
async def get_sparql_data(query: str):
    """Endpoint to query the SPARQL endpoint with a user-provided query."""
    try:
        result = sparql_client.query(query)
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))