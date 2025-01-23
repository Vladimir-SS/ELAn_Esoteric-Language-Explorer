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
            "yearCreated": result[0]["yearCreated"]["value"],
            "url": result[0]["url"]["value"],
            "shortDescription": result[0]["shortDescription"]["value"],
            "alias": result[0]["alias"]["value"] if "alias" in result[0] else None,
            "designedBy": result[0]["designedBy"]["value"] if "designedBy" in result[0] else None,
            "categories": [category["category"]["value"] for category in result] if "category" in result[0] else None
        }

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