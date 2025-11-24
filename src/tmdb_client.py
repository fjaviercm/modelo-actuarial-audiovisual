# src/tmdb_client.py

import os
import time
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv


# Carga variables del archivo .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"


class TMDBClientError(Exception):
    """Error personalizado para problemas con la API de TMDB."""
    pass


def _get(endpoint: str, params: Dict[str, Any], retries: int = 3) -> Dict[str, Any]:
    """
    Llamada genérica a la API de TMDB con reintentos y timeout ampliado.
    """
    if TMDB_API_KEY is None:
        raise TMDBClientError("TMDB_API_KEY no está definida en el archivo .env")

    url = f"{BASE_URL}/{endpoint}"
    query_params = {"api_key": TMDB_API_KEY, **params}

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=query_params, timeout=30)  # antes era 10
            resp.raise_for_status()
            return resp.json()

        except requests.exceptions.Timeout:
            print(f"[Timeout] Intento {attempt}/{retries} en {endpoint}...")
            if attempt == retries:
                raise TMDBClientError(f"Timeout final en {endpoint}")
            time.sleep(2)  # esperamos antes de reintentar

        except requests.exceptions.RequestException as e:
            print(f"[Error] {e}")
            if attempt == retries:
                raise TMDBClientError(f"Error final en {endpoint}: {e}")
            time.sleep(2)

    raise TMDBClientError("Error desconocido")


def discover_movies_by_year(year: int) -> List[Dict[str, Any]]:
    all_results: List[Dict[str, Any]] = []

    first_page = _get(
        "discover/movie",
        {
            "primary_release_year": year,
            "sort_by": "popularity.desc",
            "page": 1,
            "include_adult": "false",
        },
    )

    total_pages = first_page.get("total_pages", 1)
    print(f"Año {year}: total_pages reportado por TMDB = {total_pages}")

    all_results.extend(first_page.get("results", []))

    failed_pages = 0
    MAX_FAILED = 5   # si fallan 5 páginas seguidas, paramos

    for page in range(2, total_pages + 1):
        try:
            data = _get(
                "discover/movie",
                {
                    "primary_release_year": year,
                    "sort_by": "popularity.desc",
                    "page": page,
                    "include_adult": "false",
                },
            )
            results = data.get("results", [])
            if not results:
                break

            all_results.extend(results)
            failed_pages = 0  # reseteamos porque funcionó

        except Exception as e:
            print(f"[Página {page}] Error: {e}")
            failed_pages += 1

            if failed_pages >= MAX_FAILED:
                print(f"Demasiados errores consecutivos ({MAX_FAILED}). Parando.")
                break

            continue

        if page % 20 == 0:
            print(f"  Descargadas {page}/{total_pages} páginas...")

    return all_results


def normalize_movie(raw_movie: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza el diccionario que viene de TMDB a las columnas que nos interesan.
    Más adelante añadiremos más campos.
    """
    return {
        "tmdb_id": raw_movie.get("id"),
        "title": raw_movie.get("title"),
        "original_title": raw_movie.get("original_title"),
        "overview": raw_movie.get("overview"),
        "release_date": raw_movie.get("release_date"),
        "original_language": raw_movie.get("original_language"),
        "popularity": raw_movie.get("popularity"),
        "vote_count": raw_movie.get("vote_count"),
        "vote_average": raw_movie.get("vote_average"),
        "genre_ids": raw_movie.get("genre_ids"),
    }
