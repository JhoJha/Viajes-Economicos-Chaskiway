import requests
import pandas as pd
from pathlib import Path
from io import StringIO

# --- Coordenadas de las ciudades ---
ciudades = {
    "Lima": (-12.050, -77.042),
    "Arequipa": (-16.409, -71.537),
    "Trujillo": (-8.111, -79.028),
    "Cusco": (-13.517, -71.978),
    "Piura": (-5.194, -80.632),
    "Huancayo": (-12.066, -75.210),
    "Huaraz": (-9.530, -77.530)
}

# --- Parámetros de la API ---
start_date = "2024-07-01"
end_date = "2024-07-31"
variables = "temperature_2m,precipitation"
base_url = "https://archive-api.open-meteo.com/v1/archive"

# --- Ruta de salida (sube 3 niveles desde este archivo) ---
project_root = Path(__file__).resolve().parents[3]
output_path = project_root / "data" / "raw" / "clima"
output_path.mkdir(parents=True, exist_ok=True)

# --- DataFrame acumulador ---
df_total = pd.DataFrame()

# --- Consulta por ciudad ---
for ciudad, (lat, lon) in ciudades.items():
    print(f"🔎 Descargando clima de: {ciudad}")
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": variables,
        "timezone": "auto",
        "format": "csv"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        df["ciudad"] = ciudad
        df_total = pd.concat([df_total, df], ignore_index=True)
        print(f"✅ {ciudad}: datos cargados")

    except Exception as e:
        print(f"❌ Error con {ciudad}: {e}")

# --- Guardar CSV final ---
ruta_csv = output_path / "historico_julio_2024.csv"
df_total.to_csv(ruta_csv, index=False)
print(f"\n📁 CSV generado en: {ruta_csv}")