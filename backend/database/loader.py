import sqlite3
import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def cargar_json_desde_archivo(ruta_archivo):
    """Carga datos desde un archivo JSON, manejando errores."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                logging.warning(f"Archivo JSON está vacío, saltando: {ruta_archivo}")
                return None
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        logging.error(f"Error cargando {ruta_archivo}: {e}")
        return None

def process_redbus_data(json_dir: Path):
    """
    Lee todos los JSON de RedBus, los procesa y los devuelve como un DataFrame.
    """
    all_trips = []
    json_files = list(json_dir.glob("*.json"))
    
    if not json_files:
        logging.warning(f"No se encontraron archivos JSON en {json_dir}")
        return pd.DataFrame()

    logging.info(f"Procesando {len(json_files)} archivos JSON de RedBus...")
    
    for file_path in json_files:
        data = cargar_json_desde_archivo(file_path)

        # --- VERIFICACIÓN DE ROBUSTEZ ---
        if not data or not isinstance(data.get("inventories"), list):
            logging.warning(f"Archivo JSON inválido o sin inventario, saltando: {file_path.name}")
            continue
        
        origen = data.get("parentSrcCityName")
        destino = data.get("parentDstCityName")
        
        for viaje in data.get("inventories", []):
            fare_list = viaje.get("fareList", [])
            precios_validos = [p for p in fare_list if isinstance(p, (int, float))]
            precio_min = min(precios_validos) if precios_validos else None

            all_trips.append({
                'origen': origen,
                'destino': destino,
                'fecha_viaje': viaje.get("departureTime", " ").split(" ")[0],
                'empresa': viaje.get("travelsName"),
                'precio_min': precio_min,
                'asientos_disponibles': viaje.get("availableSeats"),
                'rating_empresa': viaje.get("totalRatings")
            })
            
    return pd.DataFrame(all_trips)


def load_combined_data_to_db(db_path: str, combined_df: pd.DataFrame):
    """
    Carga el DataFrame combinado final en la base de datos.
    """
    if combined_df.empty:
        logging.warning("El DataFrame combinado está vacío. No se cargará nada a la base de datos.")
        return

    logging.info(f"Cargando {len(combined_df)} registros en la base de datos...")
    
    conn = sqlite3.connect(db_path)
    try:
        combined_df.to_sql('viajes_combinados', conn, if_exists='replace', index=False)
        logging.info("¡Carga completada exitosamente!")
    except Exception as e:
        logging.error(f"Error al cargar datos a la base de datos: {e}")
    finally:
        conn.close()