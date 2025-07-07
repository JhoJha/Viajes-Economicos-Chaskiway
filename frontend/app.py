# frontend/app.py

import streamlit as st
# La importación debe ser relativa a la carpeta raíz del proyecto
from frontend.utils import load_data 

# Configuración de la página
st.set_page_config(
    page_title="Recomendador de Viajes",
    page_icon="🚌"
)

st.title("🚌 Recomendador de Viajes Chaskiway")
st.markdown("### ¡Bienvenido! Esta es la página principal del recomendador.")
st.markdown("Actualmente en construcción. Usa el menú de la izquierda para navegar al Dashboard.")

# Cargamos los datos para verificar que todo funciona
df = load_data()

if not df.empty:
    st.success(f"¡Conexión exitosa! Se cargaron {len(df)} registros desde utils.py.")
else:
    st.error("No se pudieron cargar los datos. Revisa la consola.")