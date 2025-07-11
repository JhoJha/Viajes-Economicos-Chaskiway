# pages/2_📊_Dashboard.py
"""
Dashboard Analítico - ChaskiWay
- Estadísticas generales del sistema
- Análisis de precios y tendencias
- Visualizaciones interactivas
- Métricas de rendimiento
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Función compartida para cargar datos
from frontend.data_loader import load_data

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="ChaskiWay | Dashboard Analítico",
    page_icon="📊",
    layout="wide",
)

# =========================
# ESTILOS CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

:root {
    --primary-color: #FF6B35;
    --secondary-color: #F7931E;
    --dark-blue: #004E89;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
    --light-gray: #F8F9FA;
    --medium-gray: #6C757D;
    --gradient-bg: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
}

.dashboard-header {
    background: var(--gradient-bg);
    padding: 2rem;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
}

.dashboard-header h1 {
    color: white;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    margin: 0;
    font-size: 2.5rem;
}

.dashboard-header p {
    color: white;
    opacity: 0.9;
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 5px solid var(--primary-color);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.metric-label {
    color: var(--medium-gray);
    font-weight: 500;
}

.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.chart-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: var(--dark-blue);
    margin-bottom: 1rem;
    font-size: 1.3rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES AUXILIARES
# =========================

@st.cache_data
def get_dashboard_data():
    """Carga y prepara los datos para el dashboard."""
    df = load_data()
    if df.empty:
        return None, None, None, None, None
    
    # Datos básicos
    df_clean = df.dropna(subset=['precio_min', 'destino'])
    
    # Estadísticas por destino
    destinos_stats = df_clean.groupby('destino').agg({
        'precio_min': ['mean', 'min', 'max', 'count'],
        'rating_empresa': 'mean',
        'asientos_disponibles': 'sum'
    }).round(2)
    
    # Estadísticas por empresa
    empresas_stats = df_clean.groupby('empresa').agg({
        'precio_min': ['mean', 'min', 'max'],
        'rating_empresa': 'mean',
        'destino': 'nunique'
    }).round(2)
    
    # Análisis temporal
    df_clean['fecha_viaje'] = pd.to_datetime(df_clean['fecha_viaje'])
    df_clean['mes'] = df_clean['fecha_viaje'].dt.month
    df_clean['dia_semana'] = df_clean['fecha_viaje'].dt.day_name()
    
    # Análisis de clima
    clima_stats = df_clean.groupby('categoria_clima').agg({
        'precio_min': ['mean', 'count'],
        'destino': 'nunique'
    }).round(2)
    
    return df_clean, destinos_stats, empresas_stats, clima_stats, df

# =========================
# CONTENIDO PRINCIPAL
# =========================

# Header del Dashboard
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Dashboard Analítico</h1>
    <p>Análisis completo de viajes y tendencias del mercado</p>
</div>
""", unsafe_allow_html=True)

# Cargar datos
df_clean, destinos_stats, empresas_stats, clima_stats, df_original = get_dashboard_data()

if df_clean is None:
    st.error("❌ No se pudieron cargar los datos. Verifica que la base de datos esté disponible.")
    st.stop()

# =========================
# MÉTRICAS PRINCIPALES
# =========================

st.markdown("### 📈 Métricas Generales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_viajes = len(df_clean)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_viajes:,}</div>
        <div class="metric-label">Total de Viajes</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    destinos_unicos = df_clean['destino'].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{destinos_unicos}</div>
        <div class="metric-label">Destinos Únicos</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    precio_promedio = df_clean['precio_min'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">S/ {precio_promedio:.0f}</div>
        <div class="metric-label">Precio Promedio</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    empresas_unicas = df_clean['empresa'].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{empresas_unicas}</div>
        <div class="metric-label">Empresas</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS Y ANÁLISIS
# =========================

# Gráfico 1: Precios por Destino
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">💰 Análisis de Precios por Destino</div>', unsafe_allow_html=True)

fig_precios = px.box(
    df_clean, 
    x='destino', 
    y='precio_min',
    title="Distribución de Precios por Destino",
    labels={'precio_min': 'Precio (S/)', 'destino': 'Destino'},
    color='destino'
)
fig_precios.update_layout(height=500, showlegend=False)
st.plotly_chart(fig_precios, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Gráfico 2: Rating de Empresas
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">⭐ Rating de Empresas de Transporte</div>', unsafe_allow_html=True)

# Filtrar empresas con suficientes datos
empresas_con_rating = df_clean.groupby('empresa')['rating_empresa'].agg(['mean', 'count']).reset_index()
empresas_con_rating = empresas_con_rating[empresas_con_rating['count'] >= 3]  # Al menos 3 viajes

if not empresas_con_rating.empty:
    fig_rating = px.bar(
        empresas_con_rating.sort_values(by='mean', ascending=True),
        x='mean',
        y='empresa',
        title="Rating Promedio por Empresa",
        labels={'mean': 'Rating Promedio', 'empresa': 'Empresa'},
        orientation='h'
    )
    fig_rating.update_layout(height=400)
    st.plotly_chart(fig_rating, use_container_width=True)
else:
    st.info("📊 No hay suficientes datos de rating para mostrar el gráfico.")
st.markdown('</div>', unsafe_allow_html=True)

# Gráfico 3: Análisis de Clima
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">🌡️ Análisis por Tipo de Clima</div>', unsafe_allow_html=True)

if 'categoria_clima' in df_clean.columns:
    clima_analysis = df_clean.groupby('categoria_clima').agg({
        'precio_min': ['mean', 'count'],
        'destino': 'nunique'
    }).round(2)
    
    fig_clima = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Precio Promedio por Clima', 'Cantidad de Viajes por Clima'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig_clima.add_trace(
        go.Bar(x=clima_analysis.index, y=clima_analysis[('precio_min', 'mean')], name="Precio Promedio"),
        row=1, col=1
    )
    
    fig_clima.add_trace(
        go.Bar(x=clima_analysis.index, y=clima_analysis[('precio_min', 'count')], name="Cantidad de Viajes"),
        row=1, col=2
    )
    
    fig_clima.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_clima, use_container_width=True)
else:
    st.info("🌡️ No hay datos de clima disponibles para el análisis.")
st.markdown('</div>', unsafe_allow_html=True)

# Gráfico 4: Disponibilidad de Asientos
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">💺 Disponibilidad de Asientos por Destino</div>', unsafe_allow_html=True)

asientos_por_destino = df_clean.groupby('destino')['asientos_disponibles'].sum().reset_index()
asientos_por_destino = asientos_por_destino.sort_values(by='asientos_disponibles', ascending=True)

fig_asientos = px.bar(
    asientos_por_destino,
    x='asientos_disponibles',
    y='destino',
    title="Total de Asientos Disponibles por Destino",
    labels={'asientos_disponibles': 'Asientos Disponibles', 'destino': 'Destino'},
    orientation='h'
)
fig_asientos.update_layout(height=400)
st.plotly_chart(fig_asientos, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABLAS DETALLADAS
# =========================

st.markdown("### 📋 Datos Detallados")

# Tabla de destinos más populares
st.markdown("#### 🏛️ Destinos Más Populares")
destinos_populares = df_clean['destino'].value_counts().head(10).reset_index()
destinos_populares.columns = ['Destino', 'Cantidad de Viajes']
st.dataframe(destinos_populares, use_container_width=True)

# Tabla de empresas con mejores precios
st.markdown("#### 💰 Empresas con Mejores Precios")
mejores_empresas = df_clean.groupby('empresa')['precio_min'].mean().sort_values().head(10).reset_index()
mejores_empresas.columns = ['Empresa', 'Precio Promedio (S/)']
mejores_empresas['Precio Promedio (S/)'] = mejores_empresas['Precio Promedio (S/)'].round(2)
st.dataframe(mejores_empresas, use_container_width=True)

# =========================
# INSIGHTS Y RECOMENDACIONES
# =========================

st.markdown("### 💡 Insights y Recomendaciones")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Mejores Oportunidades")
    
    # Destino más económico
    destino_mas_economico = df_clean.groupby('destino')['precio_min'].mean().idxmin()
    precio_minimo = df_clean.groupby('destino')['precio_min'].mean().min()
    
    st.info(f"""
    **Destino más económico:** {destino_mas_economico}
    **Precio promedio:** S/ {precio_minimo:.0f}
    """)
    
    # Empresa más económica
    empresa_mas_economica = df_clean.groupby('empresa')['precio_min'].mean().idxmin()
    precio_empresa_min = df_clean.groupby('empresa')['precio_min'].mean().min()
    
    st.info(f"""
    **Empresa más económica:** {empresa_mas_economica}
    **Precio promedio:** S/ {precio_empresa_min:.0f}
    """)

with col2:
    st.markdown("#### ⚠️ Consideraciones")
    
    # Destino más caro
    destino_mas_caro = df_clean.groupby('destino')['precio_min'].mean().idxmax()
    precio_maximo = df_clean.groupby('destino')['precio_min'].mean().max()
    
    st.warning(f"""
    **Destino más costoso:** {destino_mas_caro}
    **Precio promedio:** S/ {precio_maximo:.0f}
    """)
    
    # Destino con menos opciones
    destinos_con_menos_opciones = df_clean['destino'].value_counts().tail(3)
    st.warning(f"""
    **Destinos con menos opciones:**
    {', '.join(str(x) for x in destinos_con_menos_opciones.index.tolist())}
    """)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; font-size: 0.9rem;">
    📊 Dashboard generado automáticamente | Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}
</div>
""", unsafe_allow_html=True)
