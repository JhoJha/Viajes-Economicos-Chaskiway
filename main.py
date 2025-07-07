# main.py - El Orquestador del Proyecto Chaskiway (Versión Final)

import pandas as pd
import logging
from pathlib import Path

# Importar las funciones de nuestros módulos de backend
# Asegúrate de que tu schema.py esté actualizado con la columna 'categoria_clima'
from backend.database.schema import create_database
from backend.database.loader import process_redbus_data, load_combined_data_to_db

# --- Configuración del Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", mode='w'),
        logging.StreamHandler()
    ]
)

# --- Definición de Rutas ---
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PROCESSED_PATH = DATA_PROCESSED_DIR / "viajes_grupales.db"

# --- Función Principal (Orquestador ETL) ---

def main():
    """
    Orquesta la unión de las fuentes de datos pre-procesadas y carga el resultado
    en la base de datos SQLite final.
    """
    logging.info("🚀 --- INICIANDO PIPELINE FINAL DE INTEGRACIÓN --- 🚀")

    # --- PASO 1: EXTRACT (Leer todas las fuentes de datos) ---
    
    # 1.1 Extraer datos de RedBus (esta función ya los procesa desde los JSON)
    logging.info("Leyendo y procesando datos de RedBus...")
    df_redbus = process_redbus_data(DATA_RAW_DIR / "redbus")
    if df_redbus.empty:
        logging.critical("No se pudieron procesar los datos de RedBus. El pipeline no puede continuar.")
        return
    logging.info(f"Se procesaron {len(df_redbus)} registros de RedBus.")

    # 1.2 Extraer datos de Imágenes
    logging.info("Leyendo datos de imágenes...")
    try:
        df_imagenes = pd.read_csv(DATA_RAW_DIR / "imagenes" / "enlaces_imagenes.csv")
        df_imagenes = df_imagenes.rename(columns={'ciudad': 'destino', 'url_imagen': 'url_imagen_destino'})
        logging.info(f"Se leyeron {len(df_imagenes)} enlaces de imágenes.")
    except FileNotFoundError:
        logging.warning("No se encontró el archivo de imágenes. Se continuará sin estos datos.")
        df_imagenes = pd.DataFrame(columns=['destino', 'url_imagen_destino'])

    # 1.3 Extraer los datos de clima YA PROCESADOS
    logging.info("Leyendo datos de clima procesados...")
    try:
        df_clima = pd.read_csv(DATA_PROCESSED_DIR / "clima_final.csv")
        logging.info(f"Se leyeron {len(df_clima)} registros de clima procesado.")
    except FileNotFoundError:
        logging.critical("No se encontró 'clima_final.csv'. Por favor, ejecuta primero 'procesador_clima.py'.")
        return

    # --- PASO 2: COMBINE (MERGE) ---
    logging.info("Combinando los tres datasets...")
    
    # Unir RedBus con Clima. Las fechas ya están en formato YYYY-MM-DD en ambos.
    df_combinado = pd.merge(df_redbus, df_clima, on=['destino', 'fecha_viaje'], how='left')
    
    # Unir el resultado con Imágenes.
    df_final = pd.merge(df_combinado, df_imagenes, on='destino', how='left')
    
    logging.info(f"Total de registros combinados: {len(df_final)}. Columnas: {list(df_final.columns)}")

    # --- PASO 3: LOAD ---
    logging.info("Cargando datos combinados en la base de datos final...")
    
    # (Importante) Asegúrate de que tu schema.py tenga la columna 'categoria_clima'
    create_database(DB_PROCESSED_PATH)
    
    load_combined_data_to_db(str(DB_PROCESSED_PATH), df_final)

    logging.info("🎉 --- PIPELINE DE DATOS COMPLETADO EXITOSAMENTE --- 🎉")
    logging.info(f"Puedes encontrar la base de datos final en: {DB_PROCESSED_PATH}")

if __name__ == "__main__":
    main()