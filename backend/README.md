# 🛠️ Carpeta `backend`

Contiene todos los módulos de backend responsables de la extracción, procesamiento e integración de datos.

## Subcarpetas

- `scraping/`: Scripts para extraer datos de las fuentes (RedBus, clima, imágenes).
  - Cada subcarpeta (`redbus`, `clima`, `imagenes`) tiene su propio scraper y configuración.
- `database/`: Scripts para crear el esquema de la base de datos (`schema.py`), cargar los datos integrados (`loader.py`) y otras utilidades de integración.

## Lógica principal

- Los scrapers descargan los datos crudos y los guardan en `data/raw/`.
- El pipeline de integración (`main.py` en la raíz del proyecto) utiliza los módulos de `database/` para combinar y cargar los datos en la base de datos final.
- El backend está diseñado para ser modular y fácil de mantener.

## ¿Cómo usarlo?

1. Ejecuta los scrapers en `scraping/` para obtener los datos crudos.
2. Ejecuta `main.py` para integrar y cargar los datos en la base de datos. 