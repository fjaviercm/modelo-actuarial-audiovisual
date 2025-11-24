# src/enrich_tmdb_range.py

import sys
import time
import os
from src.enrich_tmdb_year import enrich_year

def enrich_range(start_year: int, end_year: int):
    print(f"Enriqueciendo TMDB desde {start_year} hasta {end_year}...")
    
    for year in range(start_year, end_year + 1):
        print(f"\n📆 Procesando año {year}...")

        out_path = f"data_raw/tmdb_details_{year}.csv"
        if os.path.exists(out_path):
            print(f"⚠️  Saltando año {year}: ya existe {out_path}")
            continue

        enrich_year(year)
        
        # Pausa entre años (seguro para la API)
        time.sleep(2)

    print("\n🎉 Rango completo procesado.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 -m src.enrich_tmdb_range <start_year> <end_year>")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    enrich_range(start, end)