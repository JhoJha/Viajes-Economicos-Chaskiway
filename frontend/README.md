# 🖥️ Carpeta `frontend`

Esta carpeta contiene todo el código y recursos relacionados con la interfaz de usuario de Chaskiway.

## Estructura y contenido

- `app.py`: Script principal de la aplicación web en Streamlit. Aquí se define la lógica de presentación, el buscador inteligente, el dashboard y la visualización de recomendaciones.
- `pages/`: Contiene las páginas modulares de la app, como el buscador (`1_🔍_Buscador.py`) y el dashboard de analítica (`2_📊_Dashboard.py`).
- `assets/`: Imágenes y recursos visuales usados en la interfaz (por ejemplo, el logo).
- `data_loader.py`: Utilidad para cargar los datos procesados desde la base de datos.
- `utils.py`: Funciones auxiliares para validación, formateo y utilidades visuales.
- `config.py`: Configuración de parámetros para el frontend.

## Lógica principal

- El frontend se conecta a la base de datos procesada (`data/processed/viajes_grupales.db`) y muestra recomendaciones personalizadas según el presupuesto, clima, destino y preferencias del usuario.
- Incluye visualizaciones interactivas, filtros avanzados y sugerencias inteligentes.
- El diseño prioriza la experiencia de usuario, la estética y la claridad de la información.

## ¿Cómo ejecutarlo?

```bash
streamlit run frontend/app.py
``` 