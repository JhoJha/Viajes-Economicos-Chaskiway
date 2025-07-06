# Contenido para: backend/scraping/redbus/scraper.py

import os
import json
import time
import random
import logging
import requests
from datetime import datetime

# Importar la configuración desde el mismo directorio
from .config import HEADERS, COOKIES, BODY

def scrape_redbus_route(from_city_id, to_city_id, from_name, to_name, date_str, output_dir):
    """
    Realiza scraping a la API de RedBus para una ruta y fecha específicas.
    Guarda el JSON crudo solo si la petición es exitosa (código 200).
    """
    # Validar formato de fecha
    try:
        datetime.strptime(date_str, "%d-%b-%Y")
    except ValueError:
        logging.error(f"❌ Fecha inválida: '{date_str}'. Usa 'DD-MMM-YYYY'.")
        return

    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Construir la URL y los parámetros de forma segura
    base_url = "https://www.redbus.pe/search/SearchV4Results"
    params = {
        "fromCity": from_city_id,
        "toCity": to_city_id,
        "src": from_name,
        "dst": to_name,
        "DOJ": date_str,
        "sectionId": 0, "groupId": 0, "limit": 20, "offset": 0,
        "sort": 0, "sortOrder": 0, "meta": "true", "returnSearch": 0
    }

    logging.info(f"🚌 Buscando: {from_name} -> {to_name} | Fecha: {date_str}")

    try:
        response = requests.post(
            base_url,
            params=params,
            headers=HEADERS,
            cookies=COOKIES,
            json=BODY,
            timeout=20
        )

        # Manejar códigos de estado específicos
        if response.status_code == 200:
            data = response.json()
            # Guardar el archivo JSON
            # Limpiamos el nombre de la ciudad para el nombre del archivo
            to_name_clean = to_name.replace(" (Todos)", "")
            output_path = os.path.join(output_dir, f"redbus_{to_name_clean}_{date_str}.json")
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"✅ Archivo guardado: {output_path}")

        elif response.status_code == 404:
            logging.warning(f"⚠️ Ruta no encontrada (404) para {from_name} -> {to_name} en {date_str}.")
        else:
            # Para otros errores (500, 429, etc.), mostrar un error más genérico
            logging.error(f"❌ Error en la petición: Código {response.status_code} para {from_name} -> {to_name}")
            # response.raise_for_status() # Opcional: si quieres que el programa se detenga

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error de red: {e}")
    
    # Pequeña pausa para ser respetuosos con el servidor
    time.sleep(random.uniform(1, 3))