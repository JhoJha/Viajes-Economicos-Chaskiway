# 🗄️ Carpeta `backend/database`

Esta carpeta contiene los módulos responsables de la creación, carga y gestión de la base de datos final del proyecto Chaskiway.

## Archivos principales

- `schema.py`: Define el esquema de la base de datos SQLite, incluyendo las tablas y sus columnas. Ejecuta la creación de la base de datos si no existe.
- `loader.py`: Contiene funciones para cargar los datos integrados (DataFrame) en la base de datos, asegurando la correcta inserción y actualización de registros.
- `__init__.py`: Archivo de inicialización del módulo.

## ¿Cómo se usa?

- Estos módulos son utilizados automáticamente por el pipeline principal (`main.py`) para crear la base de datos y cargar los datos combinados.
- No es necesario ejecutarlos directamente, pero puedes importar sus funciones en otros scripts si necesitas manipular la base de datos manualmente.

## Flujo típico

1. Ejecuta los scrapers y el pipeline de integración (`main.py`).
2. `main.py` usará `schema.py` para crear la base de datos y `loader.py` para cargar los datos finales.

La base de datos resultante se encuentra en `data/processed/viajes_grupales.db`. 