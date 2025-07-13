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
# FILTROS INTERACTIVOS
# =========================
st.markdown("### 🎛️ Filtros Interactivos")

# Filtro por rango de fechas
dates = pd.to_datetime(df_clean['fecha_viaje'])
min_date, max_date = dates.min(), dates.max()
fecha_inicio, fecha_fin = st.date_input(
    "Selecciona el rango de fechas:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

# Filtro por destino
destinos_opciones = ["Todos"] + sorted(df_clean['destino'].unique())
destino_seleccionado = st.selectbox("Filtrar por destino:", destinos_opciones)

# Aplicar filtros
df_filtrado = df_clean[
    (df_clean['fecha_viaje'] >= pd.to_datetime(fecha_inicio)) &
    (df_clean['fecha_viaje'] <= pd.to_datetime(fecha_fin))
]
if destino_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['destino'] == destino_seleccionado]

# =========================
# PALETA DE COLORES DE MARCA PARA PLOTLY
# =========================
PLOTLY_COLORS = ["#FF6B35", "#F7931E", "#004E89", "#28a745", "#ffc107", "#17a2b8"]

# =========================
# MÉTRICAS PRINCIPALES (compactas)
# =========================
st.markdown("""
<div style="display:flex; gap:1.2rem; justify-content:center; flex-wrap:wrap; margin-bottom:1.2rem;">
""", unsafe_allow_html=True)
for label, value, icon in [
    ("Total de Viajes", f"{total_viajes:,}", "🧳"),
    ("Destinos Únicos", destinos_unicos, "🗺️"),
    ("Precio Promedio", f"S/ {precio_promedio:.0f}", "💰"),
    ("Empresas", empresas_unicas, "🚌")
]:
    st.markdown(f"""
    <div style='background:#fff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.07); padding:0.8rem 1.5rem; min-width:160px; text-align:center; border-left:5px solid #FF6B35; margin-bottom:0.5rem;'>
        <div style='font-size:2rem; font-weight:700; color:#FF6B35; margin-bottom:0.2rem;'>{icon} {value}</div>
        <div style='color:#6C757D; font-weight:500; font-size:1.05rem;'>{label}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# GRÁFICO DE TENDENCIA DE PRECIOS (optimizado)
# =========================
if destino_seleccionado != "Todos":
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📈 Tendencia de Precios en {destino_seleccionado} a lo largo del tiempo</div>', unsafe_allow_html=True)
    df_destino = df_filtrado[df_filtrado['destino'] == destino_seleccionado]
    tendencia = df_destino.groupby('fecha_viaje')['precio_min'].mean().reset_index()
    if len(tendencia) > 50:
        st.line_chart(tendencia.set_index('fecha_viaje'))
    else:
        import plotly.express as px
        fig_tendencia = px.line(
            tendencia,
            x='fecha_viaje',
            y='precio_min',
            title=f"Tendencia de Precios en {destino_seleccionado}",
            labels={'fecha_viaje': 'Fecha', 'precio_min': 'Precio Promedio (S/)'},
            color_discrete_sequence=PLOTLY_COLORS
        )
        fig_tendencia.update_layout(height=400)
        st.plotly_chart(fig_tendencia, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# GRÁFICOS Y ANÁLISIS (top 10)
# =========================
# Gráfico 1: Precios por Destino (top 10)
destinos_top = df_filtrado['destino'].value_counts().head(10).index.tolist()
df_top_destinos = df_filtrado[df_filtrado['destino'].isin(destinos_top)]
fig_precios = px.box(
    df_top_destinos,
    x='destino',
    y='precio_min',
    title="Distribución de Precios por Destino (Top 10)",
    labels={'precio_min': 'Precio (S/)', 'destino': 'Destino'},
    color='destino',
    color_discrete_sequence=PLOTLY_COLORS
)
fig_precios.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_precios, use_container_width=True)

# Gráfico 2: Rating de Empresas (top 10)
empresas_top = df_filtrado['empresa'].value_counts().head(10).index.tolist()
empresas_con_rating = df_filtrado[df_filtrado['empresa'].isin(empresas_top)].groupby('empresa')['rating_empresa'].agg(['mean', 'count']).reset_index()
empresas_con_rating = empresas_con_rating[empresas_con_rating['count'] >= 3]
if not empresas_con_rating.empty:
    fig_rating = px.bar(
        empresas_con_rating.sort_values(by='mean', ascending=True),
        x='mean',
        y='empresa',
        title="Rating Promedio por Empresa (Top 10)",
        labels={'mean': 'Rating Promedio', 'empresa': 'Empresa'},
        orientation='h',
        color_discrete_sequence=PLOTLY_COLORS
    )
    fig_rating.update_layout(height=350)
    st.plotly_chart(fig_rating, use_container_width=True)
else:
    st.info("📊 No hay suficientes datos de rating para mostrar el gráfico.")

# Gráfico 3: Análisis de Clima (top 3)
if 'categoria_clima' in df_filtrado.columns:
    climas_top = df_filtrado['categoria_clima'].value_counts().head(3).index.tolist()
    clima_analysis = df_filtrado[df_filtrado['categoria_clima'].isin(climas_top)].groupby('categoria_clima').agg({
        'precio_min': ['mean', 'count'],
        'destino': 'nunique'
    }).round(2)
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig_clima = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Precio Promedio por Clima', 'Cantidad de Viajes por Clima'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    fig_clima.add_trace(
        go.Bar(x=clima_analysis.index, y=clima_analysis[('precio_min', 'mean')], name="Precio Promedio", marker_color=PLOTLY_COLORS[0]),
        row=1, col=1
    )
    fig_clima.add_trace(
        go.Bar(x=clima_analysis.index, y=clima_analysis[('precio_min', 'count')], name="Cantidad de Viajes", marker_color=PLOTLY_COLORS[1]),
        row=1, col=2
    )
    fig_clima.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_clima, use_container_width=True)
else:
    st.info("🌡️ No hay datos de clima disponibles para el análisis.")

# Gráfico 4: Disponibilidad de Asientos (top 10)
asientos_por_destino = df_filtrado.groupby('destino')['asientos_disponibles'].sum().reset_index()
asientos_top = asientos_por_destino.sort_values(by='asientos_disponibles', ascending=False).head(10)
import plotly.express as px
fig_asientos = px.bar(
    asientos_top,
    x='asientos_disponibles',
    y='destino',
    title="Total de Asientos Disponibles por Destino (Top 10)",
    labels={'asientos_disponibles': 'Asientos Disponibles', 'destino': 'Destino'},
    orientation='h',
    color_discrete_sequence=PLOTLY_COLORS
)
fig_asientos.update_layout(height=350)
st.plotly_chart(fig_asientos, use_container_width=True)

# =========================
# TABLAS DETALLADAS
# =========================

st.markdown("### 📋 Datos Detallados")

# Tabla de destinos más populares
st.markdown("#### 🏛️ Destinos Más Populares")
destinos_populares = df_filtrado['destino'].value_counts().head(10).reset_index()
destinos_populares.columns = ['Destino', 'Cantidad de Viajes']
st.dataframe(destinos_populares, use_container_width=True)

# Tabla de empresas con mejores precios
st.markdown("#### 💰 Empresas con Mejores Precios")
mejores_empresas = df_filtrado.groupby('empresa')['precio_min'].mean().sort_values().head(10).reset_index()
mejores_empresas.columns = ['Empresa', 'Precio Promedio (S/)']
mejores_empresas['Precio Promedio (S/)'] = mejores_empresas['Precio Promedio (S/)'].round(2)
st.dataframe(mejores_empresas, use_container_width=True)

# =========================
# TABLA DE DESTINOS POPULARES + EXPORTAR CSV
# =========================
import io
csv_buffer = io.StringIO()
destinos_populares.to_csv(csv_buffer, index=False)
st.download_button(
    label="⬇️ Descargar tabla como CSV",
    data=csv_buffer.getvalue(),
    file_name="destinos_populares.csv",
    mime="text/csv"
)

# =========================
# INSIGHTS Y RECOMENDACIONES
# =========================

st.markdown("### 💡 Insights y Recomendaciones")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Mejores Oportunidades")
    
    # Destino más económico
    destino_mas_economico = df_filtrado.groupby('destino')['precio_min'].mean().idxmin()
    precio_minimo = df_filtrado.groupby('destino')['precio_min'].mean().min()
    
    st.info(f"""
    **Destino más económico:** {destino_mas_economico}
    **Precio promedio:** S/ {precio_minimo:.0f}
    """)
    
    # Empresa más económica
    empresa_mas_economica = df_filtrado.groupby('empresa')['precio_min'].mean().idxmin()
    precio_empresa_min = df_filtrado.groupby('empresa')['precio_min'].mean().min()
    
    st.info(f"""
    **Empresa más económica:** {empresa_mas_economica}
    **Precio promedio:** S/ {precio_empresa_min:.0f}
    """)

with col2:
    st.markdown("#### ⚠️ Consideraciones")
    
    # Destino más caro
    destino_mas_caro = df_filtrado.groupby('destino')['precio_min'].mean().idxmax()
    precio_maximo = df_filtrado.groupby('destino')['precio_min'].mean().max()
    
    st.warning(f"""
    **Destino más costoso:** {destino_mas_caro}
    **Precio promedio:** S/ {precio_maximo:.0f}
    """)
    
    # Destino con menos opciones
    destinos_con_menos_opciones = df_filtrado['destino'].value_counts().tail(3)
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
