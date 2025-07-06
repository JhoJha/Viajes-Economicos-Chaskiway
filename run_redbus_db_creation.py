import logging
from pathlib import Path
import pandas as pd

# Importar las funciones que has creado para el proyecto grupal
from backend.database.schema import create_database
from backend.database.loader import process_redbus_data, load_combined_data_to_db

# --- Configuración Central ---
DB_PATH = "data/processed/viajes_grupales.db"
JSON_DIR = Path("data/raw/redbus")

def main():
    """
    Función principal que orquesta la creación de la DB solo con datos de RedBus.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("--- INICIANDO CREACIÓN DE BASE DE DATOS (SOLO REDBUS) ---")

    # 1. Crear la estructura de la DB
    logging.info(f"Paso 1: Creando/verificando esquema en: {DB_PATH}")
    create_database(DB_PATH)

    # 2. Procesar tus JSONs de RedBus
    logging.info(f"Paso 2: Procesando archivos JSON desde: {JSON_DIR}")
    df_redbus = process_redbus_data(JSON_DIR)

    if df_redbus.empty:
        logging.error("No se pudieron procesar los datos de RedBus. El proceso se detiene.")
        return

    # 3. Cargar SOLO tu DataFrame a la base de datos.
    # Para el proyecto grupal, el main.py final combinará los datos antes de este paso.
    # Aquí, solo cargamos los datos de RedBus para validar.
    logging.info("Paso 3: Cargando datos de RedBus en la base de datos...")
    
    # Añadimos las columnas faltantes con valores nulos para que coincida con el esquema
    df_redbus['temperatura_promedio'] = None
    df_redbus['clima_descripcion'] = None
    df_redbus['url_imagen_destino'] = None
    
    load_combined_data_to_db(DB_PATH, df_redbus)

    logging.info("\n✅ ¡Base de datos creada y poblada con los datos de RedBus exitosamente!")
    logging.info(f"Puedes encontrar tu base de datos en: {DB_PATH}")

if __name__ == "__main__":
    main()