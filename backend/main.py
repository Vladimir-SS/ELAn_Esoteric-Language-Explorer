from typing import List, Dict
from fastapi import FastAPI, HTTPException, Query
from src import SPARQLClient
from src import *
from src.utils import get_esolang_from_query_result
import urllib.parse
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


app = FastAPI()

sparql_client = SPARQLClient("http://host.docker.internal:3030/Esolangs/sparql") # Change to "http://localhost:3030/Esolangs/sparql" if not using Docker

@app.get("/api/esolangs", response_model=List[str])
def get_esolangs():
    """Fetch all esolangs from the SPARQL endpoint."""
    try:
        result = sparql_client.query(ESOLANGS_NAME_LIST_QUERY)
        if not result:
            logging.info("No esolangs found.")
            raise HTTPException(status_code=404, detail="No esolangs found.")
        esolangs = [esolang["name"]["value"] for esolang in result]

        return esolangs
    except Exception as e:
        logging.error(f"Error fetching esolangs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/esolangs/{esolang_name}", response_model=Dict)
async def get_esolang(esolang_name: str):
    """Fetch details of a specific esolang from the SPARQL endpoint."""
    try:
        encoded_esolang_name = urllib.parse.quote(esolang_name)
        result = sparql_client.query(create_esolang_name_query(encoded_esolang_name))
        if not result:
            logging.info(f"No data found for esolang: {esolang_name}")
            raise HTTPException(status_code=404, detail="No data found.")

        return get_esolang_from_query_result(esolang_name, result)
    except Exception as e:
        logging.error(f"Error fetching esolang: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/esolangs/search/", response_model=List[str])
async def search_esolangs(
    search_term: str,
    paradigm: List[str] = Query(None),
    category: List[str] = Query(None),
    year_created: List[str] = Query(None),
    memory_system: List[str] = Query(None),
    dimension: List[str] = Query(None),
    computational_class: List[str] = Query(None),
    file_extension: List[str] = Query(None),
    type_system: List[str] = Query(None),
    dialect: List[str] = Query(None),
    limit=20,
    offset=0,
):
    """Search for esolangs based on a search term and various filters."""
    try:
        query = create_esolang_search_query(
            search_term,
            year_created,
            paradigm,
            category,
            memory_system,
            dimension,
            computational_class,
            file_extension,
            type_system,
            dialect,
            limit,
            offset,
        )
        logging.info(f"Query: {query}")

        result = sparql_client.query(query)
        if not result:
            logging.info(f"No data found")
            raise HTTPException(status_code=404, detail="No data found")

        print("Result: ", result)
        esolangs = [esolang["name"]["value"] for esolang in result]
        return esolangs
    except Exception as e:
        logging.error(f"Error during search: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/year-created", response_model=List[str])
async def get_years_created():
    """Fetch all unique years an esolang was created from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_years_created_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        years = [year["yearCreated"]["value"] for year in result]

        return years
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/category", response_model=List[str])
async def get_categories():
    """Fetch all unique categories from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_categories_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        categories = [category["category"]["value"] for category in result]

        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/paradigm", response_model=List[str])
async def get_paradigms():
    """Fetch all unique paradigms from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_paradigms_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        paradigms = [paradigm["paradigm"]["value"] for paradigm in result]

        return paradigms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/computational-class", response_model=List[str])
async def get_computational_classes():
    """Fetch all unique computational classes from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_computational_classes_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        classes = [class_["computationalClass"]["value"] for class_ in result]

        return classes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory-system", response_model=List[str])
async def get_memory_systems():
    """Fetch all unique memory systems from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_memory_systems_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        systems = [system["memorySystem"]["value"] for system in result]

        return systems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dimension", response_model=List[str])
async def get_dimensions():
    """Fetch all unique dimensions from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_dimensions_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        dimensions = [dimension["dimension"]["value"] for dimension in result]

        return dimensions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/type-system", response_model=List[str])
async def get_type_systems():
    """Fetch all unique type systems from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_type_systems_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        systems = [system["typeSystem"]["value"] for system in result]

        return systems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dialect", response_model=List[str])
async def get_dialects():
    """Fetch all unique dialects from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_dialects_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        dialects = [dialect["dialect"]["value"] for dialect in result]

        return dialects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/file-extension", response_model=List[str])
async def get_file_extensions():
    """Fetch all unique file extensions from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_file_extensions_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        extensions = [extension["fileExtension"]["value"] for extension in result]

        return extensions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sparsql-data", response_model=List[dict])
async def get_sparql_data(query: str):
    """Endpoint to query the SPARQL endpoint with a user-provided query."""
    try:
        result = sparql_client.query(query)
        if not result:
            logging.info("No data found.")
            raise HTTPException(status_code=404, detail="No data found.")
        return result
    except Exception as e:
        logging.error(f"Error fetching SPARQL data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
