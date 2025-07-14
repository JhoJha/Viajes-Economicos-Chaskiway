# Se importan los paquetes necesarios para manejo de base de datos, archivos, logs y datos
import sqlite3           # Para interactuar con bases de datos SQLite
import pandas as pd      # Para manipulación de datos tabulares
from pathlib import Path # Para manejo de rutas de archivos
import json              # Para leer y escribir archivos JSON
import logging           # Para registrar mensajes de log

# Configura el sistema de logging para mostrar mensajes informativos con timestamp
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def cargar_json_desde_archivo(ruta_archivo):
    """
    Carga datos desde un archivo JSON, manejando errores comunes como archivo vacío,
    archivo no encontrado o errores de decodificación.
    Devuelve el contenido como diccionario o None si hay error.
    """
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
    Lee todos los archivos JSON de RedBus en el directorio especificado,
    procesa los datos de viajes y los devuelve como un DataFrame de pandas.
    Realiza verificaciones de robustez para evitar errores por datos faltantes o mal formateados.
    """
    all_trips = []  # Lista para almacenar todos los viajes procesados
    json_files = list(json_dir.glob("*.json"))  # Busca todos los archivos JSON en el directorio
    
    if not json_files:
        logging.warning(f"No se encontraron archivos JSON en {json_dir}")
        return pd.DataFrame()  # Retorna DataFrame vacío si no hay archivos

    logging.info(f"Procesando {len(json_files)} archivos JSON de RedBus...")
    
    for file_path in json_files:
        data = cargar_json_desde_archivo(file_path)

        # Verifica que el archivo tenga datos válidos y una lista de inventarios
        if not data or not isinstance(data.get("inventories"), list):
            logging.warning(f"Archivo JSON inválido o sin inventario, saltando: {file_path.name}")
            continue
        
        # Obtiene las ciudades de origen y destino del viaje
        origen = data.get("parentSrcCityName")
        destino = data.get("parentDstCityName")
        
        # Procesa cada viaje en el inventario
        for viaje in data.get("inventories", []):
            fare_list = viaje.get("fareList", [])
            # Filtra precios válidos (números) y obtiene el mínimo
            precios_validos = [p for p in fare_list if isinstance(p, (int, float))]
            precio_min = min(precios_validos) if precios_validos else None

            # Agrega los datos relevantes del viaje a la lista
            all_trips.append({
                'origen': origen,
                'destino': destino,
                'fecha_viaje': viaje.get("departureTime", " ").split(" ")[0], # Solo la fecha
                'empresa': viaje.get("travelsName"),
                'precio_min': precio_min,
                'asientos_disponibles': viaje.get("availableSeats"),
                'rating_empresa': viaje.get("totalRatings")
            })
            
    return pd.DataFrame(all_trips)  # Convierte la lista de viajes en un DataFrame


def load_combined_data_to_db(db_path: str, combined_df: pd.DataFrame):
    """
    Carga el DataFrame combinado final en la base de datos SQLite especificada por db_path.
    Si el DataFrame está vacío, no realiza ninguna acción.
    Utiliza el método to_sql de pandas para insertar los datos en la tabla 'viajes_combinados'.
    """
    if combined_df.empty:
        logging.warning("El DataFrame combinado está vacío. No se cargará nada a la base de datos.")
        return

    logging.info(f"Cargando {len(combined_df)} registros en la base de datos...")
    
    conn = sqlite3.connect(db_path)  # Abre conexión a la base de datos
    try:
        # Inserta el DataFrame en la tabla 'viajes_combinados', reemplazando si ya existe
        combined_df.to_sql('viajes_combinados', conn, if_exists='replace', index=False)
        logging.info("¡Carga completada exitosamente!")
    except Exception as e:
        logging.error(f"Error al cargar datos a la base de datos: {e}")
    finally:
        conn.close()  # Cierra la conexión a la base de