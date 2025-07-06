# Contenido para: backend/database/schema.py (Versión Grupal)

import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def create_database(db_path="data/processed/viajes_grupales.db"):
    """
    Crea una base de datos simple con una sola tabla para el proyecto.
    Esta tabla contendrá los datos ya combinados de todas las fuentes.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tabla principal que combinará toda la información
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS viajes_combinados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origen TEXT,
            destino TEXT,
            fecha_viaje DATE,
            empresa TEXT,
            precio_min REAL,
            asientos_disponibles INTEGER,
            rating_empresa REAL,
            
            -- Columnas para los datos de tus compañeros
            temperatura_promedio REAL,
            clima_descripcion TEXT,
            url_imagen_destino TEXT,

            UNIQUE(origen, destino, fecha_viaje, empresa, precio_min)
        );
        """)
        
        conn.commit()
        logging.info(f"Base de datos '{db_path}' y tabla 'viajes_combinados' verificadas/creadas.")
    except sqlite3.Error as e:
        logging.error(f"Error al crear la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Para que puedas probar este script por separado
    create_database()