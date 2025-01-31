from typing import List, Dict
from fastapi import FastAPI, HTTPException
from src import SPARQLClient
from src import (
    ESOLANGS_NAME_LIST_QUERY,
    create_esolang_name_query,
    create_esolang_search_query,
)
from src.utils import get_esolang_from_query_result
import urllib.parse

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
        encoded_esolang_name = urllib.parse.quote(esolang_name)
        result = sparql_client.query(create_esolang_name_query(encoded_esolang_name))
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")

        return get_esolang_from_query_result(esolang_name, result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/esolangs/search", response_model=List[str])
async def search_esolangs(search_term: str, limit: int = 20, offset: int = 0):
    """Search for esolangs based on a search term."""
    try:
        encoded_search_term = urllib.parse.quote(search_term)
        query = create_esolang_search_query(encoded_search_term, limit, offset)
        result = sparql_client.query(query)
        if not result:
            raise HTTPException(status_code=404, detail="No data found")

        esolangs = [esolang["name"]["value"] for esolang in result]

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
