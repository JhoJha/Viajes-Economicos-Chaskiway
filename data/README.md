# 📁 Carpeta `data`

Esta carpeta almacena todos los datos utilizados y generados por el proyecto, organizados en dos subcarpetas principales:

- `raw/`: Datos crudos extraídos directamente de las fuentes (RedBus, clima, imágenes). Aquí se almacenan los archivos JSON, CSV y otros formatos originales antes de ser procesados.
- `processed/`: Datos ya integrados y listos para ser consumidos por el frontend. Incluye la base de datos final (`viajes_grupales.db`) y archivos CSV procesados como `clima_final.csv`.

## Estructura típica

```
data/
  ├── raw/
  │   ├── redbus/         # JSONs crudos de la API interna de RedBus
  │   ├── clima/          # CSVs crudos de la API de clima
  │   └── imagenes/       # CSV con enlaces de imágenes de la API de Pixabay
  └── processed/
      ├── viajes_grupales.db  # Base de datos SQLite final
      └── clima_final.csv     # Datos de clima integrados y limpios
```

## Notas

- Los datos crudos se generan al ejecutar los scrapers.
- Los datos procesados se generan al ejecutar el pipeline principal (`main.py`). 