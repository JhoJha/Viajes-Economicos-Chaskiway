# 🖼️ Scraper de Imágenes (`backend/scraping/imagenes`)

Este módulo obtiene enlaces de imágenes representativas de los destinos usando la API de Pixabay.

## ¿Cómo funciona?
- `scraper.py`: Realiza peticiones a la API de Pixabay y guarda los enlaces de imágenes en un archivo CSV.

## ¿Cómo ejecutarlo?

```bash
python backend/scraping/imagenes/scraper.py
```

- El archivo generado es `data/raw/imagenes/enlaces_imagenes.csv`. 