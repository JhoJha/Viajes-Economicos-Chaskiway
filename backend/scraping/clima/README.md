# 🌦️ Scraper de Clima (`backend/scraping/clima`)

Este módulo descarga y procesa datos de clima para los destinos usando la API de Visual Crossing.

## ¿Cómo funciona?
- `scraper.py`: Descarga los datos crudos de clima en formato CSV.
- `procesador.py`: Limpia y transforma los datos crudos en un archivo procesado listo para integrar.

## ¿Cómo ejecutarlo?

```bash
python backend/scraping/clima/scraper.py
python backend/scraping/clima/procesador.py
```

- Los datos crudos se guardan en `data/raw/clima/`.
- El archivo procesado final se guarda en `data/processed/clima_final.csv`. 