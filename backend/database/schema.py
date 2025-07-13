# backend/database/schema.py (Versión Final Integrada)

import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def create_database(db_path="data/processed/viajes_grupales.db"):
    """
    Crea la base de datos y la tabla final del proyecto con el esquema completo.
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
            temperatura_promedio REAL,
            categoria_clima TEXT,
            url_imagen_destino TEXT,

            UNIQUE(origen, destino, fecha_viaje, empresa, precio_min)
        );
        """)
        
        conn.commit()
        logging.info(f"Base de datos '{db_path}' y tabla 'viajes_combinados' verificadas/creadas con el esquema final.")
    except sqlite3.Error as e:
        logging.error(f"Error al crear la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()