# app.py

import sys
from pathlib import Path
import streamlit as st
from datetime import date
sys.path.append(str(Path(__file__).resolve().parents[1]))
from frontend.data_loader import load_data

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="Chaskiway | Viajes desde Lima",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Destinos de fallback en caso de que no se puedan cargar desde la BD
DESTINOS_FALLBACK = ["Arequipa", "Cusco", "Trujillo", "Piura", "Huancayo", "Huaraz"]

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
    --light-gray: #F8F9FA;
    --medium-gray: #6C757D;
    --gradient-bg: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
}

/* Reset y estilos base */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero section */
.hero-section {
    background: var(--gradient-bg);
    padding: 4rem 2rem;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 3rem;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="white" opacity="0.1"><polygon points="0,0 1000,100 1000,0"/></svg>');
    background-size: cover;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 1.3rem;
    color: white;
    margin-bottom: 0;
    opacity: 0.95;
}

/* Formulario de búsqueda */
.search-form {
    background: white;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    margin: 2rem 0;
    border: 1px solid #e3e3e3;
}

.search-form h3 {
    color: var(--dark-blue);
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1.5rem;
}

/* Botón de búsqueda mejorado */
.stButton > button {
    background: var(--gradient-bg) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
    font-family: 'Poppins', sans-serif !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.6) !important;
}

/* Selectbox y date input styling */
.stSelectbox > div > div {
    background: var(--light-gray);
    border-radius: 10px;
    border: 2px solid #e3e3e3;
    transition: border-color 0.3s ease;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.stDateInput > div > div {
    background: var(--light-gray);
    border-radius: 10px;
    border: 2px solid #e3e3e3;
    transition: border-color 0.3s ease;
}

.stDateInput > div > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

/* Sección de características */
.features-section {
    margin: 4rem 0;
    padding: 2rem;
    background: var(--light-gray);
    border-radius: 20px;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transition: transform 0.3s ease;
    border: 1px solid #e3e3e3;
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.feature-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: var(--dark-blue);
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.feature-description {
    color: var(--medium-gray);
    font-size: 0.95rem;
    line-height: 1.5;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: var(--medium-gray);
    border-top: 1px solid #e3e3e3;
    margin-top: 3rem;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
    }
    
    .search-form {
        padding: 1.5rem;
    }
    
    .feature-card {
        padding: 1.5rem;
    }
}

/* Loading state */
.loading-message {
    text-align: center;
    padding: 2rem;
    color: var(--medium-gray);
    font-style: italic;
}

/* Error state */
.error-message {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES
# =========================

@st.cache_data
def get_available_destinations():
    """
    Obtiene los destinos disponibles desde la base de datos.
    Si no puede cargar los datos, usa destinos de fallback.
    """
    try:
        df = load_data()
        if not df.empty and 'destino' in df.columns:
            destinos = sorted(df['destino'].unique())
            # Filtrar destinos vacíos o None
            destinos = [d for d in destinos if d and str(d).strip()]
            return destinos if destinos else DESTINOS_FALLBACK
        else:
            return DESTINOS_FALLBACK
    except Exception as e:
        st.warning(f"No se pudieron cargar los destinos desde la base de datos. Usando destinos predeterminados.")
        return DESTINOS_FALLBACK

@st.cache_data
def get_stats_summary():
    """
    Obtiene estadísticas rápidas para mostrar en la página principal.
    """
    try:
        df = load_data()
        if not df.empty:
            total_viajes = len(df)
            empresas_unicas = df['empresa'].nunique() if 'empresa' in df.columns else 0
            precio_min = int(df['precio_min'].min()) if 'precio_min' in df.columns else 0
            destinos_unicos = df['destino'].nunique() if 'destino' in df.columns else 0
            
            return {
                'total_viajes': total_viajes,
                'empresas': empresas_unicas,
                'precio_desde': precio_min,
                'destinos': destinos_unicos
            }
        else:
            return None
    except Exception:
        return None

# =========================
# CONTENIDO PRINCIPAL
# =========================

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">🚌 Chaskiway</h1>
        <p class="hero-subtitle">Encuentra tu próximo viaje desde Lima</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Obtener destinos disponibles
available_destinations = get_available_destinations()

# Obtener estadísticas para mostrar
stats = get_stats_summary()

# Mostrar estadísticas rápidas si están disponibles
if stats:
    st.markdown("### 📊 Tenemos opciones para ti")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Viajes Disponibles",
            value=f"{stats['total_viajes']:,}",
            help="Total de opciones de viaje disponibles"
        )
    
    with col2:
        st.metric(
            label="🏛️ Destinos",
            value=stats['destinos'],
            help="Ciudades que puedes visitar"
        )
    
    with col3:
        st.metric(
            label="🚌 Empresas",
            value=stats['empresas'],
            help="Empresas de transporte disponibles"
        )
    
    with col4:
        st.metric(
            label="💰 Desde",
            value=f"S/ {stats['precio_desde']}",
            help="Precio más bajo disponible"
        )
    
    st.markdown("---")

# Formulario de búsqueda
st.markdown('<div class="search-form">', unsafe_allow_html=True)
st.markdown("### 🔍 Busca tu viaje ideal")

# Crear columnas para el formulario
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Selectbox para destino
    destino = st.selectbox(
        "¿A dónde viajas?",
        options=available_destinations,
        index=0,
        help="Selecciona tu destino preferido"
    )
    
    # Date input para fecha
    fecha = st.date_input(
        "📅 Fecha de viaje",
        value=date.today(),
        help="Selecciona cuándo quieres viajar"
    )
    
    # Botón de búsqueda
    if st.button("🔍 Buscar Viajes", use_container_width=True):
        # Validar que se hayan seleccionado opciones válidas
        if destino and fecha:
            # Guardar en session state
            st.session_state.destino = destino
            st.session_state.fecha = fecha
            
            # Mostrar mensaje de confirmación
            st.success(f"🎯 Buscando viajes a **{destino}** para el **{fecha.strftime('%d/%m/%Y')}**")
            
            # Redirigir a la página de resultados
            st.switch_page("pages/1_🔍_Buscador.py")
        else:
            st.error("❌ Por favor selecciona un destino y una fecha válidos.")

st.markdown('</div>', unsafe_allow_html=True)

# Sección de características
st.markdown("""
<div class="features-section">
    <h2 style="text-align: center; color: var(--dark-blue); font-family: 'Poppins', sans-serif; margin-bottom: 2rem;">
        ¿Por qué elegir Chaskiway?
    </h2>
</div>
""", unsafe_allow_html=True)

# Tarjetas de características
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h4 class="feature-title">Búsqueda Inteligente</h4>
        <p class="feature-description">
            Encuentra exactamente lo que buscas con nuestros filtros avanzados.
            Compara precios, horarios y servicios fácilmente.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🌡️</span>
        <h4 class="feature-title">Información Climática</h4>
        <p class="feature-description">
            Conoce el clima de tu destino para planificar mejor tu viaje.
            Información actualizada y precisa.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⭐</span>
        <h4 class="feature-title">Empresas Verificadas</h4>
        <p class="feature-description">
            Solo trabajamos with empresas confiables y bien calificadas.
            Viaja with tranquilidad y seguridad.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Botones de navegación adicionales
st.markdown("---")
st.markdown("### 🧭 Explora más opciones")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("🔍 Ver Todos los Viajes", use_container_width=True):
        st.switch_page("pages/1_🔍_Buscador.py")

with nav_col2:
    if st.button("📊 Dashboard de Viajes", use_container_width=True):
        st.switch_page("pages/2_📊_Dashboard.py")

with nav_col3:
    if st.button("ℹ️ Información", use_container_width=True):
        st.info("🚌 **Chaskiway** - Tu compañero de viajes desde Lima. Encuentra las mejores opciones de transporte terrestre con información actualizada sobre precios, horarios y clima.")

# Footer
st.markdown("""
<div class="footer">
    <p>🚌 <strong>Chaskiway</strong> - Conectando Lima con el Perú | Hecho con ❤️ y Streamlit</p>
</div>
""", unsafe_allow_html=True)

