import requests
import csv
from pathlib import Path

API_KEY = "***REMOVED_SERPAPI_KEY***"

# Búsquedas mejoradas por ciudad
CIUDADES = {
    "Arequipa": "Centro histórico de Arequipa Perú",
    "Trujillo": "Plaza de Armas Trujillo Perú",
    "Cusco": "Centro de Cusco Perú",
    "Piura": "Playa Máncora Piura Perú",
    "Huancayo": "Parque Constitución Huancayo Perú",
    "Huaraz": "Ciudad de Huaraz Perú"
}

# Ruta para guardar el CSV
PROYECTO_ROOT = Path(__file__).resolve().parents[3]
SALIDA_CSV = PROYECTO_ROOT / "data" / "raw" / "imagenes" / "enlaces_imagenes.csv"
SALIDA_CSV.parent.mkdir(parents=True, exist_ok=True)

# Diccionario final
enlaces = {}

# Scraping con SerpAPI
for ciudad, query in CIUDADES.items():
    print(f"🔎 Buscando imagen para: {ciudad}")
    params = {
        "engine": "google",
        "q": query,
        "tbm": "isch",
        "api_key": API_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()

        if "images_results" in data and data["images_results"]:
            url_imagen = data["images_results"][0]["original"]
            enlaces[ciudad] = url_imagen
            print(f"✅ {ciudad}: {url_imagen}")
        else:
            enlaces[ciudad] = "NO DISPONIBLE"
            print(f"⚠️ No se encontró imagen para {ciudad}")

    except Exception as e:
        enlaces[ciudad] = "ERROR"
        print(f"❌ Error con {ciudad}: {e}")

# Guardar CSV
with open(SALIDA_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ciudad", "url_imagen"])
    for ciudad, url in enlaces.items():
        writer.writerow([ciudad, url])

print(f"\n📁 Enlaces guardados en: {SALIDA_CSV}")