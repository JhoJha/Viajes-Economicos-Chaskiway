# 📁 Carpeta `data/raw`

Aquí se almacenan los datos crudos extraídos directamente de las fuentes originales, antes de cualquier procesamiento o integración.

## Subcarpetas

- `redbus/`: Archivos JSON descargados desde la API interna de RedBus, uno por cada destino y fecha.
- `clima/`: Archivos CSV con datos de clima descargados desde la API de Visual Crossing.
- `imagenes/`: Archivo CSV (`enlaces_imagenes.csv`) con URLs de imágenes obtenidas de la API de Pixabay.

## Uso

- Estos archivos son la materia prima para el pipeline de integración (`main.py`).
- Si falta algún archivo, ejecuta el scraper correspondiente en `backend/scraping/`. 