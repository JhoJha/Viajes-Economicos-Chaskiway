# Importa el módulo sqlite3 para interactuar con bases de datos SQLite
import sqlite3

# Importa el módulo logging para registrar mensajes informativos o de error
import logging

# Importa la clase Path del módulo pathlib para trabajar con rutas de archivos de forma flexible
from pathlib import Path

# Configura el sistema de logging: nivel INFO y formato de salida con la hora y el mensaje
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Define una función para crear la base de datos y su tabla principal
def create_database(db_path="data/processed/viajes_grupales.db"):
    """
    Crea la base de datos y la tabla final del proyecto con el esquema completo.
    """
    # Convierte la ruta del archivo a un objeto Path, para facilitar operaciones sobre archivos
    db_path = Path(db_path)

    # Crea el directorio contenedor si no existe (por ejemplo: data/processed/)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Establece la conexión con la base de datos (se crea el archivo si no existe)
        conn = sqlite3.connect(db_path)

        # Crea un cursor para ejecutar comandos SQL
        cursor = conn.cursor()
        
        # Crea la tabla 'viajes_combinados' si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS viajes_combinados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único, autoincremental
            origen TEXT,                            -- Ciudad o lugar de origen
            destino TEXT,                           -- Ciudad o lugar de destino
            fecha_viaje DATE,                       -- Fecha del viaje
            empresa TEXT,                           -- Empresa de transporte
            precio_min REAL,                        -- Precio más bajo disponible
            asientos_disponibles INTEGER,           -- Cantidad de asientos libres
            rating_empresa REAL,                    -- Calificación o puntaje de la empresa
            temperatura_promedio REAL,              -- Promedio de temperatura en el destino
            categoria_clima TEXT,                   -- Categoría del clima (ej. soleado, lluvioso, etc.)
            url_imagen_destino TEXT,                -- URL de una imagen ilustrativa del destino

            -- Restricción de unicidad para evitar duplicados: no puede haber dos registros con los mismos valores en estas columnas
            UNIQUE(origen, destino, fecha_viaje, empresa, precio_min)
        );
        """)
        
        # Guarda los cambios en la base de datos
        conn.commit()

        # Muestra un mensaje informativo indicando éxito en la creación/verificación
        logging.info(f"Base de datos '{db_path}' y tabla 'viajes_combinados' verificadas/creadas con el esquema final.")
    
    # Captura errores específicos de SQLite y los registra como error
    except sqlite3.Error as e:
        logging.error(f"Error al crear la base de datos: {e}")
    
    # Esta parte se ejecuta siempre: cierra la conexión si se abrió
    finally:
        if conn:
            conn.close()

# Si este script se ejecuta directamente (y no se importa), entonces se llama a la función para crear la base de datos
if __name__ == "__main__":
    create_database()
