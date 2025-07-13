# Este script es para ejecutar el scraper de RedBus de forma independiente.

import logging
from pathlib import Path
import json
from .scraper import scrape_redbus_route # Importa la función desde scraper.py en el mismo directorio

# Configuración del logging para ver el progreso
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """
    Función principal que orquesta el scraping de RedBus para el proyecto.
    """
    logging.info("🚀 Iniciando scraping de RedBus para el mes de Julio...")

    # Cargar la configuración de ciudades
    try:
        city_ids_path = Path(__file__).parent / "city_ids.json"
        with open(city_ids_path, "r", encoding="utf-8") as f:
            CITIES = json.load(f)
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo 'city_ids.json'. Asegúrate de que exista.")
        return

    # Parámetros fijos para el trabajo
    ORIGIN_NAME = "Lima"
    ORIGIN_ID = CITIES[ORIGIN_NAME]
    TARGET_MONTH_STR = "Jul"
    TARGET_YEAR_STR = "2025"

    # Definir la carpeta de salida
    OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "raw" / "redbus"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(f"Los archivos se guardarán en: {OUTPUT_DIR}")

    # Iterar sobre cada destino desde Lima
    for city_name, city_id in CITIES.items():
        if city_name == ORIGIN_NAME:
            continue

        logging.info(f"\n--- Procesando destino: {city_name} ---")
        
        # Scrapeamos para cada día de julio (desde el 3 hasta el 31)
        for day in range(3, 32):
            date_str = f"{day:02d}-{TARGET_MONTH_STR}-{TARGET_YEAR_STR}"
            
            # Llamamos a la función del scraper
            scrape_redbus_route(
                from_city_id=ORIGIN_ID,
                to_city_id=city_id,
                from_name=f"{ORIGIN_NAME} (Todos)",
                to_name=f"{city_name} (Todos)", # Asumimos que el nombre en la API usa "(Todos)"
                date_str=date_str,
                output_dir=OUTPUT_DIR
            )

    logging.info("\n✅ Scraping de RedBus para Julio completado.")

if __name__ == "__main__":
    main()