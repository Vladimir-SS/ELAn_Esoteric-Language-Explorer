from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Query
from src import SPARQLClient
from src import *
from src.utils import *
import urllib.parse
import logging
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sparql_client = SPARQLClient("https://fuseki-728286732053.us-central1.run.app/Esolangs/query") # Change to "http://localhost:3030/Esolangs/sparql" if not using Docker or http://host.docker.internal:3030/Esolangs/sparql if using Docker

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
    except HTTPException as e:
        logging.error(f"Error fetching esolangs: {e.detail}", exc_info=True)
        raise e
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
    except HTTPException as e:
        logging.error(f"Error fetching esolang: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching esolang: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/esolangs/search/", response_model=List[str])
async def search_esolangs(
    search_term: str = None,
    paradigm: List[str] = Query(None),
    category: List[str] = Query(None),
    year_created: List[str] = Query(None),
    memory_system: List[str] = Query(None),
    dimension: List[str] = Query(None),
    computational_class: List[str] = Query(None),
    file_extension: List[str] = Query(None),
    type_system: List[str] = Query(None),
    dialect: List[str] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
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
    except HTTPException as e:
        logging.error(f"Error during search: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Unexpected error during search: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/year-created", response_model=List[str])
async def get_years_created():
    """Fetch all unique years an esolang was created from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_years_created_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        years = [year["yearCreated"]["value"] for year in result]

        return years
    except HTTPException as e:
        logging.error(f"Error fetching years created: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching years created: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/category", response_model=List[str])
async def get_categories():
    """Fetch all unique categories from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_categories_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        categories = [category["name"]["value"] for category in result]

        return categories
    except HTTPException as e:
        logging.error(f"Error fetching categories: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching categories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/paradigm", response_model=List[str])
async def get_paradigms():
    """Fetch all unique paradigms from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_paradigms_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        paradigms = [paradigm["name"]["value"] for paradigm in result]

        return paradigms
    except HTTPException as e:
        logging.error(f"Error fetching paradigms: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching paradigms: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/computational-class", response_model=List[str])
async def get_computational_classes():
    """Fetch all unique computational classes from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_computational_classes_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        classes = [class_["name"]["value"] for class_ in result]

        return classes
    except HTTPException as e:
        logging.error(f"Error fetching computational classes: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching computational classes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory-system", response_model=List[str])
async def get_memory_systems():
    """Fetch all unique memory systems from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_memory_systems_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        systems = [system["name"]["value"] for system in result]

        return systems
    except HTTPException as e:
        logging.error(f"Error fetching memory systems: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching memory systems: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dimension", response_model=List[str])
async def get_dimensions():
    """Fetch all unique dimensions from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_dimensions_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        dimensions = [dimension["name"]["value"] for dimension in result]

        return dimensions
    except HTTPException as e:
        logging.error(f"Error fetching dimensions: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching dimensions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/type-system", response_model=List[str])
async def get_type_systems():
    """Fetch all unique type systems from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_type_systems_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        systems = [system["name"]["value"] for system in result]

        return systems
    except HTTPException as e:
        logging.error(f"Error fetching type systems: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching type systems: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dialect", response_model=List[str])
async def get_dialects():
    """Fetch all unique dialects from the SPARQL endpoint."""
    try:
        result = sparql_client.query(create_dialects_query())
        if not result:
            raise HTTPException(status_code=404, detail="No data found.")
        dialects = [dialect["name"]["value"] for dialect in result]

        return dialects
    except HTTPException as e:
        logging.error(f"Error fetching dialects: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching dialects: {e}", exc_info=True)
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
    except HTTPException as e:
        logging.error(f"Error fetching file extensions: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching file extensions: {e}", exc_info=True)
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
    except HTTPException as e:
        logging.error(f"Error fetching SPARQL data: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching SPARQL data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/esolangs/similar/{esolang_name}", response_model=List[str])
async def get_similar_esolangs(esolang_name: str):
    """Fetch similar esolangs based on the given esolang name."""
    try:
        embeddings = load_embeddings()
        if embeddings is None:
            triples = sparql_client.query(create_all_triples_query())
            embeddings = compute_embeddings(triples)

        esolang_url = f"{BASE_URI}{urllib.parse.quote(esolang_name)}"
        given_language_embedding = embeddings.get(esolang_url)
        if given_language_embedding is None:
            logging.info(f"Embedding not found for {esolang_name}")
            raise HTTPException(status_code=404, detail="Embedding not found.")
        print("Given language embedding: ", given_language_embedding)

        similarities = {
            entity: cosine_similarity([given_language_embedding], [embedding])[0][0]
            for entity, embedding in embeddings.items()
            if entity != esolang_url
        }
        similarities = {entity: float(score) for entity, score in similarities.items()}
        similar_languages = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:15]

        if not similar_languages:
            raise HTTPException(status_code=404, detail="No similar esolangs found")
        print("Similar languages: ", similar_languages)

        return [entity.replace(BASE_URI, "") for entity, _ in similar_languages]
    except HTTPException as e:
        logging.error(f"Error fetching similar esolangs: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logging.error(f"Error fetching similar esolangs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
