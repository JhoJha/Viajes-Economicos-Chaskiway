# Contenido para: frontend/pages/2_📊_Dashboard.py

import streamlit as st
import pandas as pd
import altair as alt

# Paso 1: Importar la función para cargar datos desde nuestro archivo de utilidades.
# La ruta de importación es relativa a la raíz del proyecto.
try:
    from frontend.utils import load_data
except ImportError:
    # Fallback por si se ejecuta el script directamente desde la carpeta 'pages'
    from utils import load_data

st.set_page_config(
    page_title="Dashboard Analítico",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Analítico de Viajes")
st.markdown("Análisis visual de los datos de viajes interprovinciales desde Lima.")

# Paso 2: Cargar los datos. ¡Así de fácil!
df = load_data()

# Si el dataframe está vacío, mostramos un mensaje y paramos.
if df.empty:
    st.warning("No se pudieron cargar los datos. Asegúrate de que el pipeline principal (`main.py`) se haya ejecutado.")
    st.stop()

# --- A partir de aquí, es su lienzo en blanco para crear visualizaciones ---

# --- Ejemplo 1: Métricas Principales ---
st.header("Métricas Generales")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Viajes Registrados", f"{len(df)}")
with col2:
    st.metric("Destino más Económico", df.loc[df['precio_min'].idxmin()]['destino'], f"S/ {df['precio_min'].min():.2f}")
with col3:
    # Usamos .dropna() para evitar errores si no hay ratings
    st.metric("Empresa Mejor Calificada", df.loc[df['rating_empresa'].dropna().idxmax()]['empresa'], f"{df['rating_empresa'].max()} ⭐")

st.markdown("---")

# --- Ejemplo 2: Gráfico de Precios Promedio por Destino ---
st.header("Comparativa de Precios por Destino")
precios_promedio = df.groupby('destino')['precio_min'].mean().round(2).reset_index()

chart = alt.Chart(precios_promedio).mark_bar().encode(
    x=alt.X('destino', title='Destino', sort='-y'),
    y=alt.Y('precio_min', title='Precio Promedio (S/)'),
    tooltip=['destino', 'precio_min']
).properties(
    title='Precio Promedio de Pasaje por Destino'
)
st.altair_chart(chart, use_container_width=True)


# --- Ejemplo 3: Distribución de Climas ---
st.header("Distribución de Climas en los Destinos")
clima_counts = df['categoria_clima'].value_counts().reset_index()
clima_counts.columns = ['categoria_clima', 'count']

clima_chart = alt.Chart(clima_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="count", type="quantitative"),
    color=alt.Color(field="categoria_clima", type="nominal", title="Categoría de Clima"),
    tooltip=['categoria_clima', 'count']
).properties(
    title='Proporción de Días por Tipo de Clima'
)
st.altair_chart(clima_chart, use_container_width=True)

# --- Pueden añadir más gráficos aquí ---
st.header("Datos Completos")
st.dataframe(df) # Mostramos la tabla completa al final para referencia