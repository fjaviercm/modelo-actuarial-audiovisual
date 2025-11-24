# src/enrich_tmdb_year.py

import pandas as pd
import time
import os
import sys

from src.tmdb_details import fetch_movie_details, normalize_details
from src.tmdb_client import discover_movies_by_year

def enrich_year(year: int):
    print(f"Descargando IDs de películas de {year}...")
    
    raw_movies = discover_movies_by_year(year)
    tmdb_ids = [m["id"] for m in raw_movies]

    print(f"Total películas encontradas: {len(tmdb_ids)}")

    enriched = []

    for i, tmdb_id in enumerate(tmdb_ids, start=1):
        try:
            details = fetch_movie_details(tmdb_id)
            enriched.append(normalize_details(details))
        except Exception as e:
            print(f"Error con {tmdb_id}: {e}")

        # Respetar rate-limiting
        time.sleep(0.25)

        if i % 20 == 0:
            print(f"Procesadas {i}/{len(tmdb_ids)}")

    df = pd.DataFrame(enriched)

    os.makedirs("data_raw", exist_ok=True)
    path = f"data_raw/tmdb_details_{year}.csv"
    df.to_csv(path, index=False)

    print(f"Guardado: {path} ({len(df)} filas)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 -m src.enrich_tmdb_year <year>")
        sys.exit(1)

    year = int(sys.argv[1])
    enrich_year(year)