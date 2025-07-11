# 🚌 Scraper de RedBus (`backend/scraping/redbus`)

Este módulo extrae datos de viajes interprovinciales desde la API interna de RedBus.

## ¿Cómo funciona?
- Utiliza ingeniería inversa e inspección de red para identificar la API interna de RedBus.
- Realiza peticiones POST para obtener los datos en formato JSON, evitando el scraping tradicional de HTML.

## Archivos principales
- `scraper.py`: Lógica principal para extraer los datos de la API.
- `run_scraper.py`: Script de entrada para ejecutar el scraping en lote.
- `config.py`: Configuración de headers, cookies y body para las peticiones.
- `city_ids.json`: IDs de ciudades y rutas soportadas.

## ¿Cómo ejecutarlo?

```bash
python backend/scraping/redbus/run_scraper.py
```

Los archivos JSON generados se guardan en `data/raw/redbus/`. 