# app.py

import sys
from pathlib import Path
import streamlit as st
from datetime import date
import base64
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

@st.cache_data
def get_available_destinations():
    try:
        df = load_data()
        if not df.empty and 'destino' in df.columns:
            destinos = sorted(df['destino'].unique())
            destinos = [d for d in destinos if d and str(d).strip()]
            return destinos if destinos else DESTINOS_FALLBACK
        else:
            return DESTINOS_FALLBACK
    except Exception:
        return DESTINOS_FALLBACK

@st.cache_data
def get_stats_summary():
    try:
        df = load_data()
        if not df.empty:
            total_viajes = len(df)
            empresas_unicas = df['empresa'].nunique() if 'empresa' in df.columns else 0
            precio_min = int(df['precio_min'].min()) if 'precio_min' in df.columns else 0
            precio_max = int(df['precio_min'].max()) if 'precio_min' in df.columns else 500
            destinos_unicos = df['destino'].nunique() if 'destino' in df.columns else 0
            return {
                'total_viajes': total_viajes,
                'empresas': empresas_unicas,
                'precio_min': precio_min,
                'precio_max': precio_max,
                'destinos': destinos_unicos
            }
        else:
            return None
    except Exception:
        return None

@st.cache_data
def get_climate_options():
    try:
        df = load_data()
        if not df.empty and 'categoria_clima' in df.columns:
            climas = sorted(df['categoria_clima'].unique())
            return [c for c in climas if c and str(c).strip()]
        else:
            return ["Cálido", "Templado", "Frío"]
    except Exception:
        return ["Cálido", "Templado", "Frío"]

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
    padding-top: 0rem !important;
    padding-bottom: 2rem;
}

/* Eliminar margen superior de primer hijo (hero/banner) */
.main .block-container > *:first-child {
    margin-top: 0 !important;
}

.chaski-hero {
    margin-top: 0 !important;
    margin-bottom: 1rem !important;
}

/* Hero section mejorada */
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
    margin-bottom: 0.5rem;
    opacity: 0.95;
}

.hero-tagline {
    font-family: 'Poppins', sans-serif;
    font-size: 1rem;
    color: white;
    opacity: 0.85;
    font-style: italic;
}

/* Formulario de búsqueda mejorado */
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

.search-form .form-subtitle {
    color: var(--medium-gray);
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1rem;
}

/* Campos de formulario con iconos */
.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--dark-blue);
    font-size: 1rem;
}

.form-group .help-text {
    font-size: 0.85rem;
    color: var(--medium-gray);
    margin-top: 0.3rem;
}

.required-field::after {
    content: " *";
    color: #dc3545;
    font-weight: bold;
}

.optional-field::after {
    content: " (opcional)";
    color: var(--medium-gray);
    font-size: 0.85rem;
    font-weight: normal;
}

/* Botón de búsqueda mejorado */
.search-button {
    margin-top: 1.5rem;
}

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

/* Selectbox y inputs mejorados */
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

.stNumberInput > div > div {
    background: var(--light-gray);
    border-radius: 10px;
    border: 2px solid #e3e3e3;
    transition: border-color 0.3s ease;
}

.stNumberInput > div > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

/* Alertas y mensajes */
.info-box {
    background: #e3f2fd;
    border-left: 4px solid #2196f3;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #0d47a1;
}

.warning-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #856404;
}

.success-box {
    background: #d4edda;
    border-left: 4px solid #28a745;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #155724;
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

/* Flexibility toggle */
.flexibility-toggle {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #e3e3e3;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu, header, .stApp > header {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Elimina el padding superior de la página y del hero */
.main .block-container {
    padding-top: 0.5rem !important;
}
header { margin-bottom: 0 !important; }
.chaski-hero {
    margin-top: 0.5rem !important;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# === CSS GLOBAL PARA LA PÁGINA PRINCIPAL ===
st.markdown('''
<style>
.chaski-hero {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    padding: 2.2rem 1.2rem 2.2rem 1.2rem;
    text-align: center;
    border-radius: 22px;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 32px rgba(255, 107, 53, 0.10);
    position: relative;
    overflow: visible;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.chaski-hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.10);
    display: flex;
    align-items: center;
    gap: 0.7rem;
    justify-content: center;
}
.chaski-hero-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    color: white;
    margin-bottom: 0.7rem;
    opacity: 0.95;
}
.chaski-hero-form {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    padding: 1.2rem 1.5rem 0.5rem 1.5rem;
    margin-top: 1.2rem;
    width: 100%;
    max-width: 820px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.chaski-metrics-row {
    display: flex;
    gap: 2.5rem;
    justify-content: center;
    margin: 1.2rem 0 1.5rem 0;
    flex-wrap: wrap;
}
.chaski-metric {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    padding: 0.7rem 1.2rem;
    min-width: 120px;
    text-align: center;
    margin-bottom: 0.5rem;
}
.chaski-metric-label {
    color: #FF6B35;
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    justify-content: center;
}
.chaski-metric-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #004E89;
}
@media (max-width: 900px) {
    .chaski-hero-form { padding: 0.7rem 0.5rem 0.2rem 0.5rem; }
    .chaski-metrics-row { gap: 1.2rem; }
}
</style>
''', unsafe_allow_html=True)

# === HERO + FORMULARIO ===
# Leer el logo y convertirlo a base64
with open("frontend/assets/Logo de Chaskiway_ Aventura en el Camino.png", "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode()

st.markdown(f'''
<div class="chaski-hero" style="display: flex; align-items: center; gap: 2.2rem; justify-content: center; flex-wrap: wrap;">
    <img src="data:image/png;base64,{logo_base64}" alt="Logo Chaskiway" style="height: 90px; border-radius: 18px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); background: #fff; padding: 0.3rem;" />
    <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center; min-width: 220px;">
        <div class="chaski-hero-title">🚌 Chaskiway</div>
        <div class="chaski-hero-subtitle">Tu Motor de Recomendación de Viajes<br><span style="font-size:0.98rem; font-weight:400;">Encuentra las mejores opciones según tu presupuesto y preferencias</span></div>
    </div>
    <div class="chaski-hero-form">
''', unsafe_allow_html=True)

# Obtener datos necesarios
try:
    available_destinations = get_available_destinations()
    stats = get_stats_summary()
    climate_options = get_climate_options()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.info("💡 Asegúrate de haber ejecutado el pipeline de datos")
    available_destinations = DESTINOS_FALLBACK
    stats = None
    climate_options = ["Cálido", "Templado", "Frío"]

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
            label="💰 Precios",
            value=f"S/ {stats['precio_min']} - {stats['precio_max']}",
            help="Rango de precios disponible"
        )
    
    st.markdown("---")

# Formulario de búsqueda principal
st.markdown("### 🎯 Encuentra tu viaje ideal")
st.markdown('<p class="form-subtitle">Completa tus preferencias y te mostraremos las mejores recomendaciones</p>', unsafe_allow_html=True)

# Crear columnas para el formulario
col1, col2 = st.columns(2)

with col1:
    # Campo de presupuesto (PRINCIPAL)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="required-field">💰 ¿Cuál es tu presupuesto máximo?</label>', unsafe_allow_html=True)
    
    presupuesto_min = stats['precio_min'] if stats else 30
    presupuesto_max = stats['precio_max'] if stats else 500
    
    presupuesto = st.number_input(
        label="Presupuesto",
        min_value=presupuesto_min,
        max_value=presupuesto_max * 2,  # Permitir un rango más amplio
        value=presupuesto_max,
        step=10,
        help="Ingresa el máximo que estás dispuesto a pagar por tu viaje",
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="help-text">💡 Te mostraremos las mejores opciones dentro de tu presupuesto</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Campo de fecha (OBLIGATORIO)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="required-field">📅 ¿Cuándo quieres viajar?</label>', unsafe_allow_html=True)
    
    fecha = st.date_input(
        label="Fecha de viaje",
        value=date.today(),
        help="Selecciona tu fecha preferida de viaje",
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="help-text">🔄 Buscaremos opciones en fechas cercanas si es necesario</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Campo de clima (PRINCIPAL)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="required-field">🌡️ ¿Qué tipo de clima prefieres?</label>', unsafe_allow_html=True)
    
    # Mapeo de climas con iconos y descripciones
    climate_mapping = {
        "Cálido": "🌞 Cálido (Costa - Playas y ciudades cálidas)",
        "Templado": "🌤️ Templado (Sierra - Clima moderado)",
        "Frío": "❄️ Frío (Altura - Montañas y zonas altas)"
    }
    
    # Crear opciones display
    climate_display_options = []
    for climate in climate_options:
        display_text = climate_mapping.get(climate, f"🌡️ {climate}")
        climate_display_options.append(display_text)
    
    selected_climate_display = st.selectbox(
        label="Clima preferido",
        options=climate_display_options,
        index=0,
        help="Selecciona el tipo de clima que más te gusta para tu viaje",
        label_visibility="collapsed"
    )
    
    # Extraer el clima real del display
    clima_preferido = None
    for climate in climate_options:
        if climate and selected_climate_display and climate in selected_climate_display:
            clima_preferido = climate
            break
    
    st.markdown('<div class="help-text">🎯 Priorizaremos destinos con tu clima preferido</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Campo de destino (OPCIONAL)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="optional-field">🏛️ ¿Tienes algún destino en mente?</label>', unsafe_allow_html=True)
    
    destino_options = ["Sin preferencia"] + available_destinations
    destino = st.selectbox(
        label="Destino preferido",
        options=destino_options,
        index=0,
        help="Deja en 'Sin preferencia' si quieres que te recomendemos el mejor destino",
        label_visibility="collapsed"
    )
    
    # Convertir "Sin preferencia" a None para lógica interna
    destino_preferido = None if destino == "Sin preferencia" else destino
    
    st.markdown('<div class="help-text">🗺️ Si no tienes preferencia, te recomendaremos el mejor destino</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Opción de flexibilidad
st.markdown('<div class="flexibility-toggle">', unsafe_allow_html=True)
es_flexible = st.checkbox(
    "🔄 Soy flexible con las fechas (recomendado)",
    value=True,
    help="Activar esta opción te permitirá encontrar mejores precios en fechas cercanas"
)
if es_flexible:
    st.markdown('<div class="help-text">✨ Buscaremos opciones hasta 3 días antes/después y fines de semana cercanos</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Botón de búsqueda
st.markdown('<div class="search-button">', unsafe_allow_html=True)
if st.button("🔍 Buscar Recomendaciones", use_container_width=True):
    # Validación de campos obligatorios
    errores = []
    
    if not presupuesto or presupuesto <= 0:
        errores.append("💰 El presupuesto debe ser mayor a 0")
    
    if not fecha:
        errores.append("📅 Debes seleccionar una fecha de viaje")
    
    if not clima_preferido:
        errores.append("🌡️ Debes seleccionar un tipo de clima")
    
    if errores:
        st.error("❌ **Completa los campos obligatorios:**\n" + "\n".join(f"- {error}" for error in errores))
    else:
        # Guardar en session state para el sistema de recomendación
        st.session_state.presupuesto_max = presupuesto
        st.session_state.fecha_viaje = fecha
        st.session_state.clima_preferido = clima_preferido
        st.session_state.destino_preferido = destino_preferido
        st.session_state.es_flexible = es_flexible
        
        # Mostrar mensaje de confirmación
        destino_text = f"hacia {destino_preferido}" if destino_preferido else "al mejor destino"
        flexibilidad_text = "con flexibilidad de fechas" if es_flexible else "para fecha exacta"
        
        st.success(f"""
        ✅ **Búsqueda configurada exitosamente**
        
        🎯 **Buscando recomendaciones:**
        - 💰 Presupuesto: hasta S/ {presupuesto}
        - 📅 Fecha: {fecha.strftime('%d/%m/%Y')} ({flexibilidad_text})
        - 🌡️ Clima: {clima_preferido}
        - 🏛️ Destino: {destino_text}
        
        🚀 **Redirigiendo al motor de recomendaciones...**
        """)
        
        # Información adicional
        st.markdown("""
        <div class="info-box">
            <strong>💡 Nuestro algoritmo inteligente evaluará:</strong><br>
            • Mejores precios dentro de tu presupuesto<br>
            • Opciones en tu clima preferido<br>
            • Fechas alternativas para mayor ahorro<br>
            • Empresas mejor calificadas<br>
            • Disponibilidad de asientos
        </div>
        """, unsafe_allow_html=True)
        
        # Redirigir al buscador
        try:
            st.switch_page("pages/1_🔍_Buscador.py")
        except Exception:
            st.success("✅ Datos guardados. Navega manualmente al buscador.")
            st.page_link("pages/1_🔍_Buscador.py", label="🔍 Ir al Buscador", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# === MÉTRICAS EN FILA ===
st.markdown('''
<div class="chaski-metrics-row">
    <div class="chaski-metric">
        <div class="chaski-metric-label">🧳 Viajes Disponibles</div>
        <div class="chaski-metric-value">{}</div>
    </div>
    <div class="chaski-metric">
        <div class="chaski-metric-label">🏛️ Destinos</div>
        <div class="chaski-metric-value">{}</div>
    </div>
    <div class="chaski-metric">
        <div class="chaski-metric-label">🚌 Empresas</div>
        <div class="chaski-metric-value">{}</div>
    </div>
    <div class="chaski-metric">
        <div class="chaski-metric-label">💰 Precios</div>
        <div class="chaski-metric-value">S/ {} - {}</div>
    </div>
</div>
'''.format(
    stats['total_viajes'] if stats else '--',
    stats['destinos'] if stats else '--',
    stats['empresas'] if stats else '--',
    stats['precio_min'] if stats else '--',
    stats['precio_max'] if stats else '--',
), unsafe_allow_html=True)

# Sección de características actualizada
st.markdown("""
<div class="features-section">
    <h2 style="text-align: center; color: var(--dark-blue); font-family: 'Poppins', sans-serif; margin-bottom: 2rem;">
        ¿Por qué nuestro sistema es diferente?
    </h2>
</div>
""", unsafe_allow_html=True)

# Tarjetas de características
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🤖</span>
        <h4 class="feature-title">Recomendaciones Inteligentes</h4>
        <p class="feature-description">
            Nuestro algoritmo analiza tu presupuesto, preferencias climáticas y fechas 
            para sugerir las mejores opciones personalizadas para ti.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">💰</span>
        <h4 class="feature-title">Optimización de Precios</h4>
        <p class="feature-description">
            Te mostramos cómo ahorrar dinero sugiriendo fechas alternativas y 
            comparando automáticamente todas las opciones disponibles.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h4 class="feature-title">Flexibilidad Total</h4>
        <p class="feature-description">
            Sin destino definido? Sin problema. Te recomendamos los mejores lugares 
            según tu clima preferido y presupuesto disponible.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Información adicional sobre el sistema
st.markdown("---")
st.markdown("### 🔍 ¿Cómo funciona nuestro sistema de recomendación?")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    **🎯 Algoritmo de Puntuación:**
    - **40%** Factor precio (dentro de tu presupuesto)
    - **25%** Flexibilidad de fechas (±3 días)
    - **20%** Preferencia climática
    - **10%** Calificación de la empresa
    - **5%** Disponibilidad de asientos
    """)

with info_col2:
    st.markdown("""
    **💡 Sugerencias Inteligentes:**
    - Alertas de ahorro por cambio de fecha
    - Comparativas de precio vs. calidad
    - Recomendaciones de destinos alternativos
    - Mejor momento para viajar
    """)

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
        st.info("""
        🚌 **Chaskiway** - Tu compañero inteligente de viajes desde Lima. 
        
        Nuestro sistema de recomendación analiza miles de opciones para encontrar 
        exactamente lo que necesitas según tu presupuesto y preferencias.
        
        🎯 **¿Sabías que?** En promedio, nuestros usuarios ahorran 25% al ser flexibles con las fechas.
        """)

# Footer
st.markdown("""
<div class="footer">
    <p>🚌 <strong>Chaskiway</strong> - Sistema Inteligente de Recomendación de Viajes | Hecho con ❤️ y Streamlit</p>
</div>
""", unsafe_allow_html=True)