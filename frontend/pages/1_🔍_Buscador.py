# pages/1_🔍_Buscador.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date
import math

# Importamos nuestra función compartida para cargar los datos
from frontend.data_loader import load_data


# =========================
# CONFIGURACIÓN Y ESTILOS
# =========================
st.set_page_config(
    page_title="Chaskiway | Buscador de Viajes",
    page_icon="🔍",
    layout="wide"
)

# CSS mejorado para el buscador
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

:root {
    --primary-color: #FF6B35;
    --secondary-color: #F7931E;
    --dark-blue: #004E89;
    --light-gray: #F8F9FA;
    --medium-gray: #6C757D;
    --gradient-bg: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
}

/* Header compacto */
.compact-header {
    background: var(--gradient-bg);
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: center;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(255, 107, 53, 0.3);
}

.compact-header h2 {
    color: white;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    margin: 0;
    font-size: 1.5rem;
}

/* Indicador de búsqueda activa */
.search-indicator {
    background: #e8f5e8;
    border: 1px solid #4caf50;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    color: #2e7d32;
    font-weight: 500;
}

/* Barra de búsqueda compacta */
.search-bar {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 2px solid var(--light-gray);
}

/* Tarjetas de resultados mejoradas */
.result-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 4px solid var(--primary-color);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.result-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-bg);
}

.price-tag {
    background: var(--gradient-bg);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 1.1rem;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.company-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.rating-stars {
    color: #FFD700;
    font-size: 1.1rem;
}

.availability-badge {
    background: #28a745;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}

.low-availability {
    background: #dc3545;
}

.medium-availability {
    background: #fd7e14;
}

.climate-info {
    background: #e3f2fd;
    padding: 0.5rem;
    border-radius: 8px;
    margin-top: 0.5rem;
    border-left: 3px solid #2196f3;
}

/* Contenedor de imagen optimizado */
.image-container {
    text-align: center;
    margin: 1rem 0;
    border-radius: 10px;
    overflow: hidden;
    max-height: 250px;
    background: var(--light-gray);
}

.image-container img {
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.image-container img:hover {
    transform: scale(1.02);
}

/* Filtros sidebar */
.filter-section {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Paginación */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
}

.pagination-info {
    color: var(--medium-gray);
    font-size: 0.9rem;
}

/* Estados de carga */
.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: var(--medium-gray);
}

/* Responsive */
@media (max-width: 768px) {
    .result-card {
        padding: 1rem;
    }
    
    .compact-header h2 {
        font-size: 1.2rem;
    }
    
    .image-container {
        max-height: 200px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES AUXILIARES
# =========================

def format_availability_badge(asientos):
    """Formatea el badge de disponibilidad según asientos disponibles"""
    if asientos <= 5:
        return f'<span class="availability-badge low-availability">¡Solo {asientos} asientos!</span>'
    elif asientos <= 15:
        return f'<span class="availability-badge medium-availability">{asientos} asientos</span>'
    else:
        return f'<span class="availability-badge">{asientos} asientos disponibles</span>'

def format_rating_stars(rating):
    """Convierte rating numérico a estrellas"""
    if pd.isna(rating):
        return "⭐ N/A"
    
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars + "⭐" * half_star + "☆" * empty_stars
    return f'{stars} ({rating:.1f})'

def format_climate_info(categoria, temperatura):
    """Formatea la información climática"""
    climate_icons = {
        "Cálido": "🌡️",
        "Templado": "🌤️", 
        "Frío": "❄️",
        "Muy Frío": "🥶"
    }
    
    icon = climate_icons.get(categoria, "🌡️")
    return f"{icon} {categoria} ({temperatura:.1f}°C)"

def get_destino_index(destino_buscado, opciones_destino):
    """Obtiene el índice del destino en la lista de opciones"""
    if destino_buscado == "Todos" or destino_buscado is None:
        return 0
    
    try:
        # Buscar en las opciones (excluyendo "Todos" que está en posición 0)
        destinos_sin_todos = opciones_destino[1:]  # Excluir "Todos"
        if destino_buscado in destinos_sin_todos:
            return destinos_sin_todos.index(destino_buscado) + 1  # +1 porque "Todos" está en posición 0
        else:
            return 0  # Si no se encuentra, volver a "Todos"
    except:
        return 0

@st.cache_data
def load_and_prepare_data():
    """Carga y prepara los datos con cache"""
    return load_data()

# =========================
# CARGA DE DATOS
# =========================
with st.spinner("Cargando datos de viajes..."):
    df = load_and_prepare_data()

if df.empty:
    st.error("❌ No se encontraron datos. Verifica que el pipeline de datos se haya ejecutado correctamente.")
    st.stop()

# Coordenadas para el mapa
COORDENADAS_DESTINOS = {
    "Arequipa": (-16.4090, -71.5375),
    "Trujillo": (-8.1159, -79.0299),
    "Cusco": (-13.5319, -71.9675),
    "Piura": (-5.1945, -80.6328),
    "Huancayo": (-12.0651, -75.2049),
    "Huaraz": (-9.5278, -77.5278)
}

# =========================
# OBTENER VALORES INICIALES DEL SESSION STATE
# =========================

# Leer valores de la búsqueda inicial (desde app.py)
search_destino_inicial = st.session_state.get('destino', 'Todos')
search_fecha_inicial = st.session_state.get('fecha', date.today())

# Obtener opciones de destino disponibles
opciones_destino = ["Todos"] + sorted(df['destino'].unique())

# Calcular índices iniciales
destino_index = get_destino_index(search_destino_inicial, opciones_destino)

# Mostrar indicador si viene de una búsqueda
if 'destino' in st.session_state and st.session_state.get('destino') != 'Todos':
    st.markdown(f"""
    <div class="search-indicator">
        🎯 <strong>Búsqueda activa:</strong> Resultados para {st.session_state.get('destino')} - {st.session_state.get('fecha', date.today()).strftime('%d/%m/%Y')}
    </div>
    """, unsafe_allow_html=True)

# =========================
# HEADER Y BARRA DE BÚSQUEDA
# =========================

# Header compacto
st.markdown("""
<div class="compact-header">
    <h2>🔍 Resultados de Búsqueda</h2>
</div>
""", unsafe_allow_html=True)

# Barra de búsqueda rápida
st.markdown('<div class="search-bar">', unsafe_allow_html=True)
search_col1, search_col2, search_col3, search_col4 = st.columns([2, 2, 2, 1])

with search_col1:
    search_destino = st.selectbox(
        "🏛️ Destino",
        options=opciones_destino,
        index=destino_index,
        key="search_destino"
    )

with search_col2:
    search_fecha = st.date_input(
        "📅 Fecha",
        value=search_fecha_inicial,
        key="search_fecha"
    )

with search_col3:
    search_presupuesto = st.slider(
        "💰 Presupuesto máximo",
        min_value=int(df['precio_min'].min()),
        max_value=int(df['precio_min'].max()),
        value=int(df['precio_min'].max()),
        step=10,
        key="search_presupuesto"
    )

with search_col4:
    st.markdown("<br>", unsafe_allow_html=True)
    nueva_busqueda = st.button("🔄 Nueva Búsqueda", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Si presionan nueva búsqueda, limpiar session state y volver al inicio
if nueva_busqueda:
    # Limpiar valores de búsqueda del session state
    keys_to_clear = ['destino', 'fecha', 'pagina_actual']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.switch_page("app.py")

# =========================
# SIDEBAR - FILTROS AVANZADOS
# =========================

st.sidebar.header("🎯 Filtros Avanzados")

# Filtros en sidebar
with st.sidebar:
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    # Filtro por empresa
    empresas_disponibles = sorted(df['empresa'].unique())
    empresas_seleccionadas = st.multiselect(
        "🚌 Empresas",
        options=empresas_disponibles,
        default=empresas_disponibles,
        help="Selecciona las empresas de tu preferencia",
        key="filter_empresas"
    )
    
    # Filtro por clima
    opciones_clima = sorted(df['categoria_clima'].unique())
    clima_seleccionado = st.selectbox(
        "🌡️ Tipo de Clima",
        options=["Cualquiera"] + opciones_clima,
        index=0,
        key="filter_clima"
    )
    
    # Filtro por rating
    rating_minimo = st.slider(
        "⭐ Rating mínimo",
        min_value=1.0,
        max_value=5.0,
        value=1.0,
        step=0.5,
        help="Filtra por calificación de la empresa",
        key="filter_rating"
    )
    
    # Filtro por disponibilidad
    asientos_minimos = st.slider(
        "💺 Asientos mínimos",
        min_value=1,
        max_value=50,
        value=1,
        help="Mínimo de asientos disponibles",
        key="filter_asientos"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ordenamiento
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("📊 Ordenar por:")
    
    orden_opciones = {
        "Precio (menor a mayor)": ("precio_min", True),
        "Precio (mayor a menor)": ("precio_min", False),
        "Rating (mejor a peor)": ("rating_empresa", False),
        "Disponibilidad (más asientos)": ("asientos_disponibles", False),
        "Empresa (A-Z)": ("empresa", True)
    }
    
    orden_seleccionado = st.selectbox(
        "Ordenar resultados:",
        options=list(orden_opciones.keys()),
        index=0,
        key="filter_orden"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para limpiar filtros
    if st.button("🔄 Limpiar Todos los Filtros", use_container_width=True):
        # Limpiar session state
        keys_to_clear = ['destino', 'fecha', 'pagina_actual']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Reiniciar página
        st.rerun()

# =========================
# APLICAR FILTROS
# =========================

# Empezar con el dataframe completo
df_filtrado = df.copy()

# Aplicar filtros de búsqueda rápida
if search_destino != "Todos":
    df_filtrado = df_filtrado[df_filtrado['destino'] == search_destino]

df_filtrado = df_filtrado[df_filtrado['precio_min'] <= search_presupuesto]

# Aplicar filtros del sidebar
if empresas_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['empresa'].isin(empresas_seleccionadas)]

if clima_seleccionado != "Cualquiera":
    df_filtrado = df_filtrado[df_filtrado['categoria_clima'] == clima_seleccionado]

df_filtrado = df_filtrado[df_filtrado['rating_empresa'] >= rating_minimo]
df_filtrado = df_filtrado[df_filtrado['asientos_disponibles'] >= asientos_minimos]

# Aplicar ordenamiento
columna_orden, ascendente = orden_opciones[orden_seleccionado]
df_filtrado = df_filtrado.sort_values(columna_orden, ascending=ascendente)

# =========================
# PAGINACIÓN
# =========================

# Configuración de paginación
RESULTADOS_POR_PAGINA = 10
total_resultados = len(df_filtrado)
total_paginas = math.ceil(total_resultados / RESULTADOS_POR_PAGINA)

# Inicializar página actual
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 1

# Resetear página si se cambian los filtros
if total_paginas > 0 and st.session_state.pagina_actual > total_paginas:
    st.session_state.pagina_actual = 1

# Botones de paginación en la parte superior
if total_paginas > 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Anterior", disabled=st.session_state.pagina_actual == 1):
            st.session_state.pagina_actual -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="pagination-info">
            Página {st.session_state.pagina_actual} de {total_paginas} 
            ({total_resultados} resultados encontrados)
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Siguiente ➡️", disabled=st.session_state.pagina_actual == total_paginas):
            st.session_state.pagina_actual += 1
            st.rerun()

# Calcular índices para la página actual
if total_resultados > 0:
    inicio_idx = (st.session_state.pagina_actual - 1) * RESULTADOS_POR_PAGINA
    fin_idx = inicio_idx + RESULTADOS_POR_PAGINA
    df_pagina = df_filtrado.iloc[inicio_idx:fin_idx]
else:
    df_pagina = df_filtrado

# =========================
# MOSTRAR RESULTADOS
# =========================

st.markdown("---")

if df_filtrado.empty:
    st.markdown("""
    <div class="no-results">
        <h3>😔 No se encontraron viajes</h3>
        <p>Intenta ajustar tus filtros o buscar en fechas diferentes.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Mostrar estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Opciones", len(df_filtrado))
    
    with col2:
        precio_promedio = df_filtrado['precio_min'].mean()
        st.metric("💰 Precio Promedio", f"S/ {precio_promedio:.0f}")
    
    with col3:
        mejor_rating = df_filtrado['rating_empresa'].max()
        st.metric("⭐ Mejor Rating", f"{mejor_rating:.1f}")
    
    with col4:
        empresas_unicas = df_filtrado['empresa'].nunique()
        st.metric("🚌 Empresas", empresas_unicas)
    
    st.markdown("---")
    
    # Mostrar tarjetas de resultados
    for idx, (_, viaje) in enumerate(df_pagina.iterrows()):
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0; color: var(--dark-blue); font-size: 1.3rem;">
                        🏛️ {viaje['destino']}
                    </h3>
                    <div class="company-info">
                        <span style="font-weight: 600; color: var(--medium-gray);">
                            {viaje['empresa']}
                        </span>
                        <span class="rating-stars">
                            {format_rating_stars(viaje['rating_empresa'])}
                        </span>
                    </div>
                </div>
                <div class="price-tag">
                    S/ {viaje['precio_min']:.0f}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong>📅 Fecha:</strong> {viaje['fecha_viaje'].strftime('%d/%m/%Y')}
                </div>
                <div>
                    <strong>💺 Disponibilidad:</strong><br>
                    {format_availability_badge(viaje['asientos_disponibles'])}
                </div>
            </div>
            
            <div class="climate-info">
                <strong>🌡️ Clima esperado:</strong> {format_climate_info(viaje['categoria_clima'], viaje['temperatura_promedio'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar imagen si está disponible (con tamaño controlado)
        if pd.notna(viaje['url_imagen_destino']):
            try:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(
                    viaje['url_imagen_destino'], 
                    width=300, 
                    caption=f"Vista de {viaje['destino']}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            except:
                pass  # Si la imagen no carga, continuar sin mostrar error
    
    # Botones de paginación en la parte inferior
    if total_paginas > 1:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Anterior ", disabled=st.session_state.pagina_actual == 1, key="prev_bottom"):
                st.session_state.pagina_actual -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="pagination-info">
                Página {st.session_state.pagina_actual} de {total_paginas}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("Siguiente ➡️ ", disabled=st.session_state.pagina_actual == total_paginas, key="next_bottom"):
                st.session_state.pagina_actual += 1
                st.rerun()

# =========================
# MAPA DE DESTINOS
# =========================

if not df_filtrado.empty:
    st.markdown("---")
    st.header("🗺️ Ubicación de los Destinos")
    
    # Crear mapa solo con destinos filtrados
    destinos_mapa = df_filtrado.groupby('destino').agg({
        'precio_min': 'min',
        'empresa': 'count'
    }).reset_index()
    destinos_mapa.columns = ['destino', 'precio_min', 'opciones']
    
    # Centramos el mapa en Perú
    mapa = folium.Map(
        location=[-9.19, -75.01], 
        zoom_start=5, 
        tiles="CartoDB positron"
    )
    
    for _, row in destinos_mapa.iterrows():
        ciudad = row["destino"]
        if ciudad in COORDENADAS_DESTINOS:
            folium.Marker(
                location=COORDENADAS_DESTINOS[ciudad],
                popup=f"""
                <b>{ciudad}</b><br>
                Desde S/{row['precio_min']:.0f}<br>
                {row['opciones']} opciones disponibles
                """,
                tooltip=f"{ciudad} - {row['opciones']} opciones",
                icon=folium.Icon(color='red', icon='bus', prefix='fa')
            ).add_to(mapa)
    
    st_folium(mapa, width="100%", height=400)

# =========================
# FOOTER CON ACCIONES
# =========================

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 Volver al Inicio", use_container_width=True):
        # Limpiar session state al volver al inicio
        keys_to_clear = ['destino', 'fecha', 'pagina_actual']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("app.py")

with col2:
    if st.button("📊 Ver Dashboard", use_container_width=True):
        st.switch_page("pages/2_📊_Dashboard.py")

with col3:
    if st.button("🔄 Nueva Búsqueda", use_container_width=True):
        # Limpiar session state para nueva búsqueda
        keys_to_clear = ['destino', 'fecha', 'pagina_actual']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("app.py")