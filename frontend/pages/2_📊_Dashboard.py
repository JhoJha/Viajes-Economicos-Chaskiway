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
import io

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

.stMetric {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES AUXILIARES
# =========================

@st.cache_data
def get_dashboard_data():
    """Carga y prepara los datos para el dashboard."""
    try:
        df = load_data()
        if df is None or df.empty:
            st.warning("⚠️ No se encontraron datos en la base de datos.")
            return None, None, None, None, None
        
        # Validar columnas necesarias
        required_columns = ['precio_min', 'destino', 'empresa', 'fecha_viaje']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"❌ Columnas faltantes en los datos: {missing_columns}")
            return None, None, None, None, None
        
        # Limpiar datos
        df_clean = df.dropna(subset=['precio_min', 'destino'])
        
        # Convertir fecha_viaje a datetime
        df_clean['fecha_viaje'] = pd.to_datetime(df_clean['fecha_viaje'], errors='coerce')
        df_clean = df_clean.dropna(subset=['fecha_viaje'])
        
        # Validar que los precios sean numéricos y positivos
        df_clean['precio_min'] = pd.to_numeric(df_clean['precio_min'], errors='coerce')
        df_clean = df_clean[df_clean['precio_min'] > 0]
        
        if df_clean.empty:
            st.warning("⚠️ No hay datos válidos después de la limpieza.")
            return None, None, None, None, None
        
        # Estadísticas por destino
        destinos_stats = df_clean.groupby('destino').agg({
            'precio_min': ['mean', 'min', 'max', 'count'],
            'rating_empresa': 'mean' if 'rating_empresa' in df_clean.columns else None,
            'asientos_disponibles': 'sum' if 'asientos_disponibles' in df_clean.columns else None
        }).round(2)
        
        # Estadísticas por empresa
        empresas_stats = df_clean.groupby('empresa').agg({
            'precio_min': ['mean', 'min', 'max'],
            'rating_empresa': 'mean' if 'rating_empresa' in df_clean.columns else None,
            'destino': 'nunique'
        }).round(2)
        
        # Análisis temporal
        df_clean['mes'] = df_clean['fecha_viaje'].dt.month
        df_clean['dia_semana'] = df_clean['fecha_viaje'].dt.day_name()
        
        # Análisis de clima (si existe la columna)
        clima_stats = None
        if 'categoria_clima' in df_clean.columns:
            clima_stats = df_clean.groupby('categoria_clima').agg({
                'precio_min': ['mean', 'count'],
                'destino': 'nunique'
            }).round(2)
        
        return df_clean, destinos_stats, empresas_stats, clima_stats, df
        
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None, None, None, None, None

def safe_mean(series):
    """Calcula la media de manera segura."""
    if series is None or series.empty:
        return 0
    return series.mean()

def safe_count(series):
    """Cuenta elementos de manera segura."""
    if series is None or series.empty:
        return 0
    return len(series)

def safe_nunique(series):
    """Cuenta elementos únicos de manera segura."""
    if series is None or series.empty:
        return 0
    return series.nunique()

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
with st.spinner("Cargando datos..."):
    df_clean, destinos_stats, empresas_stats, clima_stats, df_original = get_dashboard_data()

if df_clean is None or df_clean.empty:
    st.error("❌ No se pudieron cargar los datos. Verifica que la base de datos esté disponible.")
    st.stop()

# =========================
# FILTROS INTERACTIVOS
# =========================
st.markdown("### 🎛️ Filtros Interactivos")

col1, col2 = st.columns(2)

with col1:
    # Filtro por rango de fechas
    dates = pd.to_datetime(df_clean['fecha_viaje'])
    min_date, max_date = dates.min(), dates.max()
    
    # Convertir a objetos date para Streamlit
    min_date_obj = min_date.date()
    max_date_obj = max_date.date()
    
    fecha_range = st.date_input(
        "Selecciona el rango de fechas:",
        value=(min_date_obj, max_date_obj),
        min_value=min_date_obj,
        max_value=max_date_obj,
        format="DD/MM/YYYY"
    )

with col2:
    # Filtro por destino
    destinos_opciones = ["Todos"] + sorted(df_clean['destino'].unique())
    destino_seleccionado = st.selectbox("Filtrar por destino:", destinos_opciones)

# Verificar que se seleccionaron dos fechas
if len(fecha_range) == 2:
    fecha_inicio, fecha_fin = fecha_range
else:
    fecha_inicio, fecha_fin = min_date_obj, max_date_obj

# Aplicar filtros
df_filtrado = df_clean[
    (df_clean['fecha_viaje'] >= pd.to_datetime(fecha_inicio)) &
    (df_clean['fecha_viaje'] <= pd.to_datetime(fecha_fin))
]

if destino_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['destino'] == destino_seleccionado]

# =========================
# PALETA DE COLORES
# =========================
PLOTLY_COLORS = ["#FF6B35", "#F7931E", "#004E89", "#28a745", "#ffc107", "#17a2b8"]

# =========================
# MÉTRICAS PRINCIPALES
# =========================

if not df_filtrado.empty:
    # Calcular métricas
    total_viajes = len(df_filtrado)
    destinos_unicos = safe_nunique(df_filtrado['destino'])
    precio_promedio = safe_mean(df_filtrado['precio_min'])
    empresas_unicas = safe_nunique(df_filtrado['empresa'])
    
    # Mostrar métricas en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🧳 Total de Viajes",
            value=f"{total_viajes:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="🗺️ Destinos Únicos",
            value=destinos_unicos,
            delta=None
        )
    
    with col3:
        st.metric(
            label="💰 Precio Promedio",
            value=f"S/ {precio_promedio:.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🚌 Empresas",
            value=empresas_unicas,
            delta=None
        )

    st.markdown("---")

    # =========================
    # GRÁFICOS Y ANÁLISIS
    # =========================

    # Gráfico de tendencia de precios
    if destino_seleccionado != "Todos":
        st.markdown("#### 📈 Tendencia de Precios")
        df_tendencia = df_filtrado.groupby('fecha_viaje')['precio_min'].mean().reset_index()
        
        if len(df_tendencia) > 1:
            fig_tendencia = px.line(
                df_tendencia,
                x='fecha_viaje',
                y='precio_min',
                title=f"Tendencia de Precios en {destino_seleccionado}",
                labels={'fecha_viaje': 'Fecha', 'precio_min': 'Precio Promedio (S/)'},
                color_discrete_sequence=PLOTLY_COLORS
            )
            fig_tendencia.update_layout(height=400)
            st.plotly_chart(fig_tendencia, use_container_width=True)
        else:
            st.info("📊 No hay suficientes datos para mostrar la tendencia de precios.")

    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de precios por destino
        st.markdown("#### 💰 Precios por Destino")
        destinos_top = df_filtrado['destino'].value_counts().head(10).index.tolist()
        df_top_destinos = df_filtrado[df_filtrado['destino'].isin(destinos_top)]
        
        if not df_top_destinos.empty:
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
            fig_precios.update_xaxes(tickangle=45)
            st.plotly_chart(fig_precios, use_container_width=True)

    with col2:
        # Gráfico de rating de empresas
        st.markdown("#### ⭐ Rating de Empresas")
        if 'rating_empresa' in df_filtrado.columns:
            empresas_top = df_filtrado['empresa'].value_counts().head(10).index.tolist()
            empresas_rating = df_filtrado[df_filtrado['empresa'].isin(empresas_top)]
            empresas_rating = empresas_rating.groupby('empresa')['rating_empresa'].agg(['mean', 'count']).reset_index()
            empresas_rating = empresas_rating[empresas_rating['count'] >= 3]
            
            if not empresas_rating.empty:
                empresas_sorted = empresas_rating.sort_values(by='mean', ascending=True)
                fig_rating = px.bar(
                    empresas_sorted,
                    x='mean',
                    y='empresa',
                    title="Rating Promedio por Empresa (Top 10)",
                    labels={'mean': 'Rating Promedio', 'empresa': 'Empresa'},
                    orientation='h',
                    color_discrete_sequence=PLOTLY_COLORS
                )
                fig_rating.update_layout(height=400)
                st.plotly_chart(fig_rating, use_container_width=True)
            else:
                st.info("📊 No hay suficientes datos de rating para mostrar.")
        else:
            st.info("📊 No hay datos de rating disponibles.")

    # Análisis de clima y asientos disponibles
    col3, col4 = st.columns(2)

    with col3:
        # Análisis de clima
        if 'categoria_clima' in df_filtrado.columns:
            st.markdown("#### 🌡️ Análisis por Clima")
            clima_data = df_filtrado.groupby('categoria_clima').agg({
                'precio_min': 'mean',
                'destino': 'count'
            }).reset_index()
            clima_data.columns = ['Clima', 'Precio Promedio', 'Cantidad Viajes']
            
            if not clima_data.empty:
                fig_clima = px.bar(
                    clima_data,
                    x='Clima',
                    y='Precio Promedio',
                    title="Precio Promedio por Clima",
                    color_discrete_sequence=PLOTLY_COLORS
                )
                fig_clima.update_layout(height=400)
                st.plotly_chart(fig_clima, use_container_width=True)
        else:
            st.info("🌡️ No hay datos de clima disponibles.")

    with col4:
        # Disponibilidad de asientos
        if 'asientos_disponibles' in df_filtrado.columns:
            st.markdown("#### 💺 Asientos Disponibles")
            asientos_data = df_filtrado.groupby('destino')['asientos_disponibles'].sum().reset_index()
            asientos_top = asientos_data.nlargest(10, 'asientos_disponibles')
            
            if not asientos_top.empty:
                fig_asientos = px.bar(
                    asientos_top,
                    x='asientos_disponibles',
                    y='destino',
                    title="Asientos Disponibles por Destino",
                    labels={'asientos_disponibles': 'Asientos', 'destino': 'Destino'},
                    orientation='h',
                    color_discrete_sequence=PLOTLY_COLORS
                )
                fig_asientos.update_layout(height=400)
                st.plotly_chart(fig_asientos, use_container_width=True)
        else:
            st.info("💺 No hay datos de asientos disponibles.")

    # =========================
    # TABLAS DETALLADAS
    # =========================

    st.markdown("### 📋 Datos Detallados")

    col1, col2 = st.columns(2)

    with col1:
        # Tabla de destinos más populares
        st.markdown("#### 🏛️ Destinos Más Populares")
        destinos_populares = df_filtrado['destino'].value_counts().head(10).reset_index()
        destinos_populares.columns = ['Destino', 'Cantidad de Viajes']
        st.dataframe(destinos_populares, use_container_width=True, height=300)

    with col2:
        # Tabla de empresas con mejores precios
        st.markdown("#### 💰 Empresas con Mejores Precios")
        empresas_precios = df_filtrado.groupby('empresa')['precio_min'].mean().reset_index()
        empresas_precios.columns = ['Empresa', 'Precio Promedio (S/)']
        empresas_precios['Precio Promedio (S/)'] = empresas_precios['Precio Promedio (S/)'].round(2)
        empresas_precios = empresas_precios.sort_values('Precio Promedio (S/)').head(10)
        st.dataframe(empresas_precios, use_container_width=True, height=300)

    # Botón para descargar datos
    st.markdown("#### 📥 Exportar Datos")
    csv_buffer = io.StringIO()
    df_filtrado.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Descargar datos filtrados como CSV",
        data=csv_buffer.getvalue(),
        file_name=f"chaskiway_datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

    # =========================
    # INSIGHTS Y RECOMENDACIONES
    # =========================

    st.markdown("### 💡 Insights y Recomendaciones")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎯 Mejores Oportunidades")
        
        try:
            # Destino más económico
            destino_economico = df_filtrado.groupby('destino')['precio_min'].mean().idxmin()
            precio_minimo = df_filtrado.groupby('destino')['precio_min'].mean().min()
            
            st.success(f"""
            **Destino más económico:** {destino_economico}  
            **Precio promedio:** S/ {precio_minimo:.0f}
            """)
            
            # Empresa más económica
            empresa_economica = df_filtrado.groupby('empresa')['precio_min'].mean().idxmin()
            precio_empresa_min = df_filtrado.groupby('empresa')['precio_min'].mean().min()
            
            st.success(f"""
            **Empresa más económica:** {empresa_economica}  
            **Precio promedio:** S/ {precio_empresa_min:.0f}
            """)
        except Exception as e:
            st.error(f"Error al calcular insights: {str(e)}")

    with col2:
        st.markdown("#### ⚠️ Consideraciones")
        
        try:
            # Destino más caro
            destino_caro = df_filtrado.groupby('destino')['precio_min'].mean().idxmax()
            precio_maximo = df_filtrado.groupby('destino')['precio_min'].mean().max()
            
            st.warning(f"""
            **Destino más costoso:** {destino_caro}  
            **Precio promedio:** S/ {precio_maximo:.0f}
            """)
            
            # Destino con menos opciones
            destinos_menos_opciones = df_filtrado['destino'].value_counts().tail(3)
            if not destinos_menos_opciones.empty:
                st.info(f"""
                **Destinos con menos opciones:**  
                {', '.join(destinos_menos_opciones.index.tolist())}
                """)
        except Exception as e:
            st.error(f"Error al calcular consideraciones: {str(e)}")

else:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados.")
    st.info("Intenta ajustar los filtros para obtener resultados.")

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6C757D; font-size: 0.9rem;">
    📊 Dashboard generado automáticamente | Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}
</div>
""", unsafe_allow_html=True)