# backend/scraping/imagenes/procesador.py

import sqlite3
import pandas as pd
from pathlib import Path  # Importación clave para manejar rutas

# --- 1. CONFIGURACIÓN DE RUTAS (LA FORMA CORRECTA Y PORTABLE) ---

# Calcula la ruta a la raíz del proyecto dinámicamente.
# Como este script está en backend/scraping/imagenes/, necesitamos subir 4 niveles.
try:
    project_root = Path(__file__).resolve().parents[3]
except IndexError:
    # Fallback por si se ejecuta desde un lugar inesperado
    project_root = Path(".").resolve()


# Define la ruta del archivo de entrada (que está en la raíz del proyecto)
input_db_path = project_root / "peru_images.db"

# Define la ruta del archivo de salida (siguiendo la estructura del proyecto)
output_db_path = project_root / "data" / "processed" / "viajes_filtrados.db"

# (Buena práctica) Asegurarse de que el directorio de salida exista
output_db_path.parent.mkdir(parents=True, exist_ok=True)

print(f"Ruta de entrada: {input_db_path}")
print(f"Ruta de salida: {output_db_path}")


# --- 2. LÓGICA DE PROCESAMIENTO ---

# Diccionario de departamentos a filtrar y sus IDs
departamentos_ids = {
    "Lima": 195105,
    "Arequipa": 195106,
    "Trujillo": 195256,
    "Cusco": 195730,
    "Piura": 195260,
    "Huancayo": 195712,
    "Huaraz": 195685
}

def normalizar_destino(destino):
    """
    Compara un nombre de destino con la lista de departamentos
    y devuelve el nombre estandarizado si encuentra una coincidencia.
    """
    if not isinstance(destino, str):
        return None  # Maneja casos donde el destino no es texto
    for dep in departamentos_ids:
        if dep.lower() in destino.lower():
            return dep
    return destino # Devuelve el original si no hay coincidencia

try:
    # Conectar y leer la base de datos de entrada usando 'with' para cierre automático
    with sqlite3.connect(input_db_path) as conn:
        print("\nLeyendo datos de la base de datos de imágenes...")
        # Es más seguro verificar si la tabla existe primero
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='viajes';")
        if cursor.fetchone() is None:
            raise ValueError("La tabla 'viajes' no fue encontrada en la base de datos de entrada.")
        
        query = "SELECT * FROM viajes"
        df = pd.read_sql_query(query, conn)

    # Normalizar y filtrar los datos
    print("Normalizando y filtrando destinos...")
    df["destino_normalizado"] = df["destino"].apply(normalizar_destino)
    df_filtrado = df[df["destino_normalizado"].isin(departamentos_ids.keys())].copy()
    print(f"Se encontraron y filtraron {len(df_filtrado)} registros.")

    # --- 3. EXPORTAR RESULTADOS ---
    if not df_filtrado.empty:
        # Guardar el DataFrame filtrado en una nueva base de datos
        with sqlite3.connect(output_db_path) as nueva_conn:
            print(f"Guardando datos filtrados en '{output_db_path.name}'...")
            df_filtrado.to_sql("viajes_filtrados", nueva_conn, index=False, if_exists="replace")
        
        print(f"\n✅ ¡Éxito! Base de datos exportada en la carpeta 'data/processed'.")
    else:
        print("\n⚠️ No se encontraron datos para exportar después del filtrado.")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo de base de datos de entrada en la ruta esperada: {input_db_path}")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")

