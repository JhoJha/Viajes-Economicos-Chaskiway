# backend/scraping/clima/procesador.py (Versión Robusta)

import pandas as pd
from pathlib import Path
import sys

# --- Búsqueda dinámica de la raíz del proyecto ---
# Esto permite ejecutar el script desde cualquier lugar
try:
    # Sube 3 niveles desde la ubicación del script (clima -> scraping -> backend -> RAÍZ)
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except IndexError:
    print("❌ ERROR: No se pudo determinar la raíz del proyecto. Asegúrate de que la estructura de carpetas sea correcta.")
    sys.exit(1) # Detiene el script con un código de error

# Agregamos la raíz al path para que pueda encontrar otros módulos si fuera necesario
sys.path.append(str(PROJECT_ROOT))


print("🚀 Iniciando pre-procesamiento del archivo de clima...")
print(f"Raíz del proyecto detectada en: {PROJECT_ROOT}")

# --- 1. CONFIGURACIÓN DE RUTAS (Ahora relativas a la raíz correcta) ---
INPUT_CSV_PATH = PROJECT_ROOT / "data" / "raw" / "clima" / "historico_julio_2024.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_CSV_PATH = OUTPUT_DIR / "clima_final.csv"

# ... (El resto del código es exactamente el mismo que te di en la respuesta anterior) ...

# Asegurarse de que el directorio de salida exista
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- 2. LECTURA Y LIMPIEZA INICIAL ---
try:
    print(f"Leyendo archivo de entrada: {INPUT_CSV_PATH}")
    df = pd.read_csv(INPUT_CSV_PATH)
    
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    df = df.rename(columns={
        'temperature_2m (°C)': 'temperatura_c',
        'Destino': 'destino'
    })

    required_cols = ['time', 'temperatura_c', 'destino']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Faltan columnas necesarias. Se esperaban: {required_cols}, pero se encontraron: {list(df.columns)}")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo de entrada. Asegúrate de que exista en: {INPUT_CSV_PATH}")
    exit()
except Exception as e:
    print(f"❌ Ocurrió un error leyendo o limpiando el CSV: {e}")
    exit()

# --- 3. TRANSFORMACIÓN DE DATOS ---
print("Transformando datos: cambiando año, calculando promedios...")

df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].map(lambda dt: dt.replace(year=2025))
df['fecha_viaje'] = df['time'].dt.strftime('%Y-%m-%d')
df['temperatura_c'] = pd.to_numeric(df['temperatura_c'], errors='coerce')
df.dropna(subset=['temperatura_c'], inplace=True)
df_promedio = df.groupby(['destino', 'fecha_viaje'])['temperatura_c'].mean().reset_index()
df_promedio = df_promedio.rename(columns={'temperatura_c': 'temperatura_promedio'})

# --- 4. ENRIQUECIMIENTO DE DATOS (AÑADIR CATEGORÍA) ---
print("Añadiendo categoría de clima...")

def categorizar_clima(temperatura: float) -> str:
    if pd.isna(temperatura): return "No disponible"
    if temperatura >= 22: return "Cálido"
    if 15 <= temperatura < 22: return "Templado"
    return "Frío"

df_promedio['categoria_clima'] = df_promedio['temperatura_promedio'].apply(categorizar_clima)
df_promedio['temperatura_promedio'] = df_promedio['temperatura_promedio'].round(2)

# --- 5. GUARDAR EL RESULTADO FINAL ---
try:
    print(f"Guardando archivo procesado en: {OUTPUT_CSV_PATH}")
    df_promedio.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\n✅ ¡Éxito! Se ha generado el archivo 'clima_final.csv' con {len(df_promedio)} filas.")
    print("Columnas del archivo final:", list(df_promedio.columns))

except Exception as e:
    print(f"❌ Ocurrió un error al guardar el archivo final: {e}")