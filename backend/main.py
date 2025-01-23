from typing import List, Dict
from fastapi import FastAPI, HTTPException
from src import SPARQLClient
from src import ESOLANG_QUERY, ESOLANG_NAME_QUERY

app = FastAPI()

sparql_client = SPARQLClient("http://host.docker.internal:3030/Esolangs/sparql") # Change to "http://localhost:3030/Esolangs/sparql" if not using Docker

@app.get("/")
def get_esolangs():
    """Fetch all esolangs from the SPARQL endpoint."""
    try:
        result = sparql_client.query(ESOLANG_NAME_QUERY)
        if not result:
            raise HTTPException(status_code=404, detail="No esolangs found.")
        esolangs = [esolang["name"]["value"] for esolang in result]
        return esolangs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/esolangs", response_model=List[Dict])
async def get_esolangs():
    """Fetch all esolangs from the SPARQL endpoint."""
    try:
        result = sparql_client.query(ESOLANG_QUERY)
        if not result:
            raise HTTPException(status_code=404, detail="No esolangs found.")

        esolangs = [
            {
                "esolang": esolang["esolang"]["value"],
                "yearCreated": esolang["yearCreated"]["value"],
                "url": esolang["url"]["value"],
                "shortDescription": esolang["shortDescription"]["value"]
            }
            for esolang in result
        ]

        return esolangs
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