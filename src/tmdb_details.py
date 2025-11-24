import os
import time
import requests
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

class TMDBClientError(Exception):
    pass

def fetch_movie_details(tmdb_id: int) -> Dict[str, Any]:
    """Obtiene detalles completos de una película, incluyendo status y keywords."""
    if TMDB_API_KEY is None:
        raise TMDBClientError("TMDB_API_KEY no está definida en el archivo .env")

    url = f"{BASE_URL}/movie/{tmdb_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "keywords",
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    if resp.status_code != 200:
        raise TMDBClientError(
            f"Error {resp.status_code} en movie/{tmdb_id}: {resp.text[:200]}"
        )

    return resp.json()

def _extract_keywords(d: Dict[str, Any]) -> str | None:
    """
    Extrae la lista de keywords como string separado por comas.
    TMDB puede devolverlas como:
      - d["keywords"] = {"keywords": [ {id, name}, ... ]}
      - o, en algunos casos, una lista directa.
    """
    kw_block = d.get("keywords")

    if kw_block is None:
        return None

    kw_list: List[Dict[str, Any]] = []

    if isinstance(kw_block, dict):
        # Caso típico de movie: {"keywords": [...]}
        kw_list = kw_block.get("keywords", []) or kw_block.get("results", [])
    elif isinstance(kw_block, list):
        kw_list = kw_block
    else:
        kw_list = []

    names = [k.get("name") for k in kw_list if isinstance(k, dict) and k.get("name")]
    if not names:
        return None

    return ", ".join(names)

def normalize_details(d: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza los detalles que consideramos importantes."""
    return {
        "tmdb_id": d.get("id"),
        "imdb_id": d.get("imdb_id"),
        "title": d.get("title"),
        "original_title": d.get("original_title"),
        "overview": d.get("overview"),
        "release_date": d.get("release_date"),
        "runtime": d.get("runtime"),
        "budget": d.get("budget"),
        "revenue": d.get("revenue"),
        "adult": d.get("adult"),

        # Clasificación artística
        "genres": ", ".join([g["name"] for g in d.get("genres", [])]) if d.get("genres") else None,

        # Producción
        "production_countries": ", ".join(
            [c["name"] for c in d.get("production_countries", [])]
        ) if d.get("production_countries") else None,
        "production_companies": ", ".join(
            [c["name"] for c in d.get("production_companies", [])]
        ) if d.get("production_companies") else None,

        # Popularidad / votos
        "popularity": d.get("popularity"),
        "vote_count": d.get("vote_count"),
        "vote_average": d.get("vote_average"),
        "original_language": d.get("original_language"),

        # Franquicia
        "belongs_to_collection": d.get("belongs_to_collection", {}).get("name")
            if d.get("belongs_to_collection") else None,

        # Estado de la película (Released, Post Production, etc.)
        "status": d.get("status"),

        # Keywords normalizadas
        "keywords": _extract_keywords(d),
    }