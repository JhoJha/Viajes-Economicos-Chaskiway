# frontend/utils.py

import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Usamos el decorador de cache de Streamlit para que la base de datos
# solo se lea una vez, sin importar cuántas veces se llame a esta función
# desde diferentes páginas. Esto hace la app súper rápida.
@st.cache_data
def load_data():
    """
    Carga los datos desde la base de datos SQLite final y los prepara para la app.
    Esta es la ÚNICA función que se conecta a la base de datos.
    """
    try:
        # La ruta se calcula desde la ubicación de este archivo (utils.py)
        # .parents[1] sube un nivel (de 'frontend/' a la raíz del proyecto)
        db_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "viajes_grupales.db"
        
        # Conectarse a la base de datos
        conn = sqlite3.connect(db_path)
        
        # Leer la tabla completa en un DataFrame de Pandas
        df = pd.read_sql_query("SELECT * FROM viajes_combinados", conn)
        
        # Cerrar la conexión
        conn.close()
        
        # --- Pequeñas conversiones para asegurar la calidad de los datos ---
        # Convertir la columna de fecha a un objeto datetime de Pandas
        df['fecha_viaje'] = pd.to_datetime(df['fecha_viaje'])
        
        # Asegurarse de que las columnas numéricas sean del tipo correcto (int/float)
        numeric_cols = ['precio_min', 'asientos_disponibles', 'rating_empresa', 'temperatura_promedio']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce') # 'coerce' convierte errores en NaN

        return df
    
    except Exception as e:
        # Si algo falla, se mostrará un error claro en la app
        st.error(f"Error crítico al cargar los datos: {e}")
        # Devolvemos un DataFrame vacío para evitar que la app se rompa más adelante
        return pd.DataFrame()