# pages/1_🔍_Buscador.py
"""
Buscador Inteligente de Viajes - ChaskiWay
- Sistema de recomendación con scoring avanzado
- Búsqueda flexible con fechas alternativas
- Sugerencias inteligentes de ahorro
- Algoritmo de ranking personalizado
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date, datetime, timedelta
import math
import numpy as np

# Función compartida para cargar datos
from frontend.data_loader import load_data

# === CSS GLOBAL PARA TODO EL FRONTEND ===
st.markdown('''
<style>
body {
    background: #f8f9fa !important;
}

/* Tarjeta de recomendación */
.chaski-card {
    max-width: 750px;
    margin: 2rem auto 1rem auto;
    background: #fff;
    border-radius: 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 1.2rem 1.5rem;
    gap: 1.5rem;
    border: 1.5px solid #f3f3f3;
    transition: box-shadow 0.2s, transform 0.2s;
    position: relative;
}
.chaski-card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
    transform: translateY(-2px) scale(1.01);
}
.chaski-card-badge {
    position: absolute;
    top: 18px;
    right: 18px;
    background: linear-gradient(90deg, #FF6B35 60%, #FFD700 100%);
    color: #fff;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.4rem 1.1rem;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(255,107,53,0.10);
    z-index: 2;
    cursor: pointer;
}
.chaski-card-badge[title]:hover {
    filter: brightness(1.1);
}
.chaski-card-img {
    width: 210px;
    height: 130px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    display: block;
}
.chaski-card-caption {
    text-align:center;
    color:#6C757D;
    font-size:0.95rem;
    margin-top:0.5rem;
}
@media (max-width: 900px) {
    .chaski-card {
        flex-direction: column !important;
        align-items: stretch !important;
        padding: 1rem 0.5rem !important;
    }
    .chaski-card-img {
        width: 100% !important;
        height: auto !important;
        max-width: 350px !important;
        margin: 0 auto !important;
    }
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f3f4f8 !important;
    border-right: 2px solid #e3e3e3;
}

/* Encabezados y separadores */
.chaski-section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #FF6B35;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.chaski-separator {
    border: none;
    border-top: 1.5px solid #e3e3e3;
    margin: 2rem 0 1.5rem 0;
}

/* Badge de coincidencia */
.chaski-badge {
    display: inline-block;
    background: linear-gradient(90deg, #28a745 60%, #6ee7b7 100%);
    color: #fff;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 0.3rem 1rem;
    border-radius: 14px;
    margin-bottom: 0.5rem;
    margin-top: 0.2rem;
    box-shadow: 0 1px 4px rgba(40,167,69,0.08);
    cursor: pointer;
}
.chaski-badge[title]:hover {
    filter: brightness(1.1);
}

/* Tooltip */
.chaski-tooltip {
    position: relative;
    display: inline-block;
}
.chaski-tooltip .chaski-tooltiptext {
    visibility: hidden;
    width: 180px;
    background-color: #333;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 0.5rem;
    position: absolute;
    z-index: 10;
    bottom: 125%;
    left: 50%;
    margin-left: -90px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.95rem;
}
.chaski-tooltip:hover .chaski-tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Animación de carga */
.chaski-loader {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
}
.chaski-loader-bus {
    font-size: 2.5rem;
    animation: chaski-bounce 1.2s infinite alternate;
}
@keyframes chaski-bounce {
    0% { transform: translateY(0); }
    100% { transform: translateY(-12px); }
}
</style>
''', unsafe_allow_html=True)

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="ChaskiWay | Buscador Inteligente",
    page_icon="🔍",
    layout="wide",
)

# =========================
# ESTILOS CSS MEJORADOS
# =========================
st.markdown(
    """
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

/* === Componentes de Recomendación === */
.smart-header {
    background: var(--gradient-bg);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
}
.smart-header h1 {
    color: #fff;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    margin: 0;
    font-size: 2rem;
}
.smart-header p {
    color: #fff;
    opacity: 0.9;
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
}

.search-summary {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
    border: 2px solid var(--success-color);
    border-radius: 15px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    color: #155724;
    font-weight: 500;
}

.recommendation-card {
    background: #fff;
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 6px solid var(--primary-color);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.recommendation-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
.recommendation-card.top-pick {
    border-left-color: #FFD700;
    background: linear-gradient(135deg, #fff9c4 0%, #fff 100%);
}
.recommendation-card.top-pick::before {
    content: '👑';
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 1.5rem;
}

.score-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: var(--gradient-bg);
    color: #fff;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
}

.price-comparison {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 10px;
    padding: 0.8rem;
    margin-top: 1rem;
    color: #856404;
    font-weight: 500;
}

.savings-alert {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 10px;
    padding: 0.8rem;
    margin-top: 1rem;
    color: #155724;
    font-weight: 500;
}

.flexibility-suggestion {
    background: #cce5ff;
    border: 1px solid #99d6ff;
    border-radius: 10px;
    padding: 0.8rem;
    margin-top: 1rem;
    color: #004085;
    font-weight: 500;
}

.match-indicators {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.match-badge {
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 600;
}
.match-perfect { background: #28a745; color: #fff; }
.match-good { background: #17a2b8; color: #fff; }
.match-ok { background: #ffc107; color: #000; }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.no-results {
    text-align: center;
    padding: 3rem;
    background: #f8f9fa;
    border-radius: 15px;
    margin: 2rem 0;
}

.trip-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.detail-item {
    background: #f8f9fa;
    padding: 0.8rem;
    border-radius: 10px;
    border-left: 4px solid var(--primary-color);
}

.availability-badge.low-availability {
    background: #dc3545;
    color: #fff;
    padding: 0.2rem 0.5rem;
    border-radius: 10px;
    font-size: 0.8rem;
}

.availability-badge.medium-availability {
    background: #ffc107;
    color: #000;
    padding: 0.2rem 0.5rem;
    border-radius: 10px;
    font-size: 0.8rem;
}

.map-container {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
</style>
    """,
    unsafe_allow_html=True,
)

# =========================
# FUNCIONES DE RECOMENDACIÓN
# =========================

def calculate_score(row, user_preferences):
    """
    Algoritmo de scoring avanzado para recomendaciones
    Considera: presupuesto, fecha, clima, disponibilidad, rating
    """
    score = 0
    
    # 1. SCORE POR PRESUPUESTO (40% del peso total)
    precio_ratio = row['precio_min'] / user_preferences['presupuesto_max']
    if precio_ratio <= 0.7:  # Muy económico
        score += 40
    elif precio_ratio <= 0.85:  # Dentro del presupuesto
        score += 30
    elif precio_ratio <= 1.0:  # Justo en el límite
        score += 20
    else:  # Sobre presupuesto
        score += 0
    
    # 2. SCORE POR FECHA (25% del peso total)
    fecha_usuario = user_preferences['fecha_viaje']
    fecha_viaje = row['fecha_viaje']
    dias_diferencia = abs((fecha_viaje - fecha_usuario).days)
    
    if dias_diferencia == 0:  # Fecha exacta
        score += 25
    elif dias_diferencia <= 1:  # ±1 día
        score += 20
    elif dias_diferencia <= 3:  # ±3 días
        score += 15
    elif dias_diferencia <= 7:  # Misma semana
        score += 10
    else:  # Más de una semana
        score += 5
    
    # 3. SCORE POR CLIMA (20% del peso total)
    if user_preferences['clima_preferido'] == 'Sin preferencia':
        score += 15  # Neutral
    elif row['categoria_clima'] == user_preferences['clima_preferido']:
        score += 20  # Coincidencia perfecta
    else:
        score += 10  # No coincide
    
    # 4. SCORE POR RATING (10% del peso total)
    rating_normalizado = (row['rating_empresa'] - 1) / 4  # Normalizar 1-5 a 0-1
    score += rating_normalizado * 10
    
    # 5. SCORE POR DISPONIBILIDAD (5% del peso total)
    if row['asientos_disponibles'] >= 30:
        score += 5
    elif row['asientos_disponibles'] >= 15:
        score += 3
    else:
        score += 1
    
    return round(score, 1)

def get_flexible_dates(fecha_base, dias_flexibilidad=7):
    """Genera rango de fechas flexibles"""
    fechas = []
    for i in range(-dias_flexibilidad, dias_flexibilidad + 1):
        fecha = fecha_base + timedelta(days=i)
        fechas.append(fecha)
    return fechas

def generate_savings_suggestions(df_recomendado, user_preferences):
    """Genera sugerencias inteligentes de ahorro"""
    sugerencias = []
    
    # 1. Ahorro por flexibilidad de fecha
    fechas_flexibles = get_flexible_dates(user_preferences['fecha_viaje'], 3)
    df_flexible = df_recomendado[df_recomendado['fecha_viaje'].isin(fechas_flexibles)]
    
    if not df_flexible.empty:
        df_fecha_exacta = df_recomendado[df_recomendado['fecha_viaje'] == user_preferences['fecha_viaje']]
        if not df_fecha_exacta.empty:
            precio_fecha_exacta = df_fecha_exacta['precio_min'].min()
            precio_minimo_flexible = df_flexible['precio_min'].min()
            
            if precio_minimo_flexible < precio_fecha_exacta:
                ahorro = precio_fecha_exacta - precio_minimo_flexible
                mejor_fecha = df_flexible[df_flexible['precio_min'] == precio_minimo_flexible].iloc[0]['fecha_viaje']
                dias_diff = abs((mejor_fecha - user_preferences['fecha_viaje']).days)
                
                sugerencias.append({
                    'tipo': 'ahorro_fecha',
                    'mensaje': f"💡 Ahorra S/ {ahorro:.0f} viajando {dias_diff} día(s) {'antes' if mejor_fecha < user_preferences['fecha_viaje'] else 'después'}",
                    'fecha_sugerida': mejor_fecha,
                    'ahorro': ahorro
                })
    
    # 2. Alternativas de empresa
    for _, viaje in df_recomendado.iterrows():
        # Encontrar la misma ruta con empresas más baratas
        misma_ruta = df_recomendado[
            (df_recomendado['destino'] == viaje['destino']) & 
            (df_recomendado['fecha_viaje'] == viaje['fecha_viaje'])
        ]
        
        if len(misma_ruta) > 1:
            # Encontrar la opción más barata en la misma ruta
            opcion_mas_barata = misma_ruta.loc[misma_ruta['precio_min'].idxmin()]
            
            if opcion_mas_barata['precio_min'] < viaje['precio_min']:
                ahorro = viaje['precio_min'] - opcion_mas_barata['precio_min']
                sugerencias.append({
                    'tipo': 'alternativa_empresa',
                    'mensaje': f"🚌 Alternativa más económica: {opcion_mas_barata['empresa']} a {viaje['destino']} por S/ {opcion_mas_barata['precio_min']:.0f} (ahorro de S/ {ahorro:.0f})",
                    'empresa': opcion_mas_barata['empresa'],
                    'ahorro': ahorro
                })
    
    # 3. Ofertas de fin de semana
    hoy = date.today()
    proximo_fin_semana = hoy + timedelta(days=(4 - hoy.weekday()) % 7)  # Viernes
    if proximo_fin_semana >= hoy:
        df_fin_semana = df_recomendado[
            (df_recomendado['fecha_viaje'] >= proximo_fin_semana) &
            (df_recomendado['fecha_viaje'] <= proximo_fin_semana + timedelta(days=2))  # Viernes a domingo
        ]
        
        if not df_fin_semana.empty:
            mejor_oferta = df_fin_semana.loc[df_fin_semana['precio_min'].idxmin()]
            ahorro_potencial = df_fin_semana['precio_min'].mean() - mejor_oferta['precio_min']
            
            if ahorro_potencial > 0:
                sugerencias.append({
                    'tipo': 'oferta_fin_semana',
                    'mensaje': f"🎉 ¡Oferta de fin de semana! Viaja a {mejor_oferta['destino']} con {mejor_oferta['empresa']} por S/ {mejor_oferta['precio_min']:.0f} (ahorra S/ {ahorro_potencial:.0f})",
                    'ahorro': ahorro_potencial
                })
    
    # Eliminar duplicados y limitar a 3 sugerencias
    unique_sugerencias = []
    seen = set()
    for s in sugerencias:
        key = (s['tipo'], s['mensaje'])
        if key not in seen:
            seen.add(key)
            unique_sugerencias.append(s)
    
    return unique_sugerencias[:3]

def get_match_level(score):
    """Determina el nivel de coincidencia basado en el score"""
    if score >= 85:
        return "match-perfect", "🎯 Coincidencia Perfecta"
    elif score >= 70:
        return "match-good", "✅ Muy Buena Opción"
    elif score >= 50:
        return "match-ok", "⚡ Opción Viable"
    else:
        return "match-ok", "📋 Disponible"

# =========================
# FUNCIONES AUXILIARES
# =========================

def format_rating_stars(rating: float) -> str:
    """Devuelve estrellas Unicode según rating de 1–5"""
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "☆" * (half + empty)

def format_availability_badge(asientos: int):
    if asientos >= 30:
        return "", f"{asientos} asientos disponibles"
    elif 10 <= asientos < 30:
        return "medium-availability", f"{asientos} asientos"
    else:
        return "low-availability", f"{asientos} restante(s)"

def format_climate_info(clima: str, temp: float) -> str:
    icon = "🌞" if clima == "Cálido" else "☁️" if clima == "Templado" else "❄️"
    return f"{icon} {clima} ({temp:.1f}°C)"

@st.cache_data
def load_and_prepare_data():
    df = load_data()
    df["fecha_viaje"] = pd.to_datetime(df["fecha_viaje"], errors="coerce").dt.date
    # Filtrar fechas pasadas
    hoy = date.today()
    df = df[df["fecha_viaje"] >= hoy]
    return df

# =========================
# CARGA DE DATOS
# =========================
with st.spinner("🔄 Cargando datos y preparando recomendaciones..."):
    try:
        df = load_and_prepare_data()
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.info("💡 Asegúrate de haber ejecutado el pipeline de datos con 'python main.py'")
        st.stop()

if df.empty:
    st.error("❌ No se encontraron datos. Verifica el pipeline de ETL.")
    st.info("📋 Pasos para solucionar:")
    st.markdown("""
    1. Ejecuta `python main.py` para procesar los datos
    2. Verifica que exista el archivo `data/processed/viajes_grupales.db`
    3. Asegúrate de que los scrapers hayan generado datos
    """)
    st.stop()

# =========================
# RECUPERAR PARÁMETROS DE BÚSQUEDA
# =========================
# Verificar si hay parámetros de búsqueda del formulario principal
required_keys = ['presupuesto_max', 'fecha_viaje', 'clima_preferido']
if not all(key in st.session_state for key in required_keys):
    st.warning("⚠️ No se encontraron parámetros de búsqueda. Redirigiendo al formulario principal...")
    st.info("Por favor, completa el formulario de búsqueda en la página principal.")
    if st.button("🏠 Ir al Formulario Principal"):
        st.switch_page("app.py")
    st.stop()

# Validar presupuesto positivo
if st.session_state['presupuesto_max'] <= 0:
    st.error("❌ El presupuesto debe ser un valor positivo")
    st.stop()

# Extraer parámetros del session state
user_preferences = {
    'presupuesto_max': st.session_state.get('presupuesto_max', 500),
    'fecha_viaje': st.session_state.get('fecha_viaje', date.today()),
    'clima_preferido': st.session_state.get('clima_preferido', 'Sin preferencia'),
    'destino_preferido': st.session_state.get('destino_preferido', 'Sin preferencia')
}

# =========================
# HEADER INTELIGENTE
# =========================
st.markdown(
    f"""
<div class="smart-header">
    <h1>🎯 Recomendaciones Inteligentes</h1>
    <p>Hemos encontrado las mejores opciones para ti basadas en tus preferencias</p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# RESUMEN DE BÚSQUEDA
# =========================
fecha_str = user_preferences['fecha_viaje'].strftime('%d/%m/%Y')
destino_str = user_preferences['destino_preferido'] if user_preferences['destino_preferido'] != 'Sin preferencia' else 'Cualquier destino'

st.markdown(
    f"""
<div class="search-summary">
    <strong>🔍 Tu búsqueda:</strong> {destino_str} | 📅 {fecha_str} | 💰 Hasta S/ {user_preferences['presupuesto_max']} | 🌡️ {user_preferences['clima_preferido']}
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# APLICAR FILTROS Y SCORING - VERSIÓN MEJORADA
# =========================

# 1. Filtrado flexible y tolerante
filtros_aplicados = []
df_filtrado = df[df['precio_min'] <= user_preferences['presupuesto_max'] * 1.2].copy(deep=True)
filtros_aplicados.append('💰 Precio ≤ 120% presupuesto')

# Filtrar por destino solo si el usuario eligió uno específico
destino_preferido = user_preferences.get('destino_preferido')
if destino_preferido and destino_preferido not in [None, '', 'Sin preferencia']:
    df_filtrado = df_filtrado[df_filtrado['destino'] == destino_preferido]
    filtros_aplicados.append(f'📍 Destino: {destino_preferido}')

# Si no hay resultados, relaja filtros progresivamente
def relajar_filtros(df, user_preferences, filtros_aplicados):
    # 1. Aumenta el rango de precio
    df_relax = df[df['precio_min'] <= user_preferences['presupuesto_max'] * 1.5]
    if not df_relax.empty:
        filtros_aplicados.append('💰 Precio ≤ 150% presupuesto (relajado)')
        return df_relax, filtros_aplicados
    # 2. Ignora clima preferido
    if user_preferences['clima_preferido'] != 'Sin preferencia':
        df_relax = df[df['precio_min'] <= user_preferences['presupuesto_max'] * 1.5]
        filtros_aplicados.append('🌡️ Clima ignorado (relajado)')
        if not df_relax.empty:
            return df_relax, filtros_aplicados
    # 3. Ignora destino preferido
    if user_preferences['destino_preferido'] != 'Sin preferencia':
        df_relax = df[df['precio_min'] <= user_preferences['presupuesto_max'] * 1.5]
        filtros_aplicados.append('📍 Destino ignorado (relajado)')
        if not df_relax.empty:
            return df_relax, filtros_aplicados
    return df_relax, filtros_aplicados

if df_filtrado.empty:
    df_filtrado, filtros_aplicados = relajar_filtros(df, user_preferences, filtros_aplicados)

if df_filtrado.empty:
    st.error("❌ No se encontraron viajes ni relajando los filtros. Prueba con otros valores.")
    st.stop()

# Resetear índice para evitar conflictos
df_filtrado = df_filtrado.reset_index(drop=True)

# Eliminar columna 'score' si ya existe
if 'score' in df_filtrado.columns:
    df_filtrado = df_filtrado.drop('score', axis=1)

# Aplicar scoring de forma segura
try:
    df_filtrado.loc[:, 'score'] = df_filtrado.apply(
        lambda row: calculate_score(row, user_preferences), axis=1
    )
except Exception as e:
    st.error(f"❌ Error al calcular puntuaciones: {str(e)}")
    st.stop()

# Ordenar por score descendente
df_filtrado = df_filtrado.sort_values('score', ascending=False)

# Tomar top 20 para análisis
df_top = df_filtrado.head(20)

# Mostrar explicación de filtros aplicados
txt_filtros = ' | '.join(filtros_aplicados)
st.info(f"🔎 Filtros aplicados: {txt_filtros}")

# =========================
# SIDEBAR - FILTROS SECUNDARIOS
# =========================
st.sidebar.header("🎛️ Ajustar Recomendaciones")

with st.sidebar:
    st.markdown("### 🔧 Filtros Avanzados")
    
    # Flexibilidad de fechas
    flexibilidad_fechas = st.slider(
        "📅 Flexibilidad de fechas (±días)",
        min_value=0,
        max_value=14,
        value=7,
        help="Incluir fechas cercanas para más opciones"
    )
    
    # Filtro por empresas
    empresas_disponibles = sorted(df_top['empresa'].unique()) if not df_top.empty else []
    empresas_seleccionadas = st.multiselect(
        "🚌 Empresas preferidas",
        options=empresas_disponibles,
        default=empresas_disponibles,
        help="Selecciona las empresas de tu confianza"
    )
    
    # Rating mínimo
    rating_minimo = st.slider(
        "⭐ Rating mínimo",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Calidad mínima del servicio"
    )
    
    # Asientos mínimos
    asientos_minimos = st.slider(
        "💺 Asientos mínimos disponibles",
        min_value=1,
        max_value=30,
        value=5,
        help="Disponibilidad mínima requerida"
    )

# Aplicar filtros secundarios
if not df_top.empty:
    fechas_flexibles = get_flexible_dates(user_preferences['fecha_viaje'], flexibilidad_fechas)
    df_final = df_top[
        (df_top['fecha_viaje'].isin(fechas_flexibles)) &
        (df_top['empresa'].isin(empresas_seleccionadas)) &
        (df_top['rating_empresa'] >= rating_minimo) &
        (df_top['asientos_disponibles'] >= asientos_minimos)
    ]
else:
    df_final = pd.DataFrame()

# =========================
# ESTADÍSTICAS Y SUGERENCIAS
# =========================
if not df_final.empty:
    # Estadísticas generales
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Opciones Recomendadas", len(df_final))
    with col2:
        precio_promedio = df_final['precio_min'].mean()
        st.metric("💰 Precio Promedio", f"S/ {precio_promedio:.0f}")
    with col3:
        mejor_score = df_final['score'].max()
        st.metric("⭐ Mejor Puntuación", f"{mejor_score:.1f}/100")
    with col4:
        empresas_count = df_final['empresa'].nunique()
        st.metric("🚌 Empresas Disponibles", empresas_count)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generar sugerencias de ahorro
    sugerencias = generate_savings_suggestions(df_final, user_preferences)
    
    if sugerencias:
        st.markdown("### 💡 Sugerencias Inteligentes")
        for sugerencia in sugerencias:
            if sugerencia['tipo'] == 'ahorro_fecha':
                st.markdown(
                    f"""
                <div class="flexibility-suggestion">
                    {sugerencia['mensaje']} ({sugerencia['fecha_sugerida'].strftime('%d/%m/%Y')})
                </div>
                """,
                    unsafe_allow_html=True
                )
            elif sugerencia['tipo'] == 'alternativa_empresa':
                st.markdown(
                    f"""
                <div class="flexibility-suggestion">
                    {sugerencia['mensaje']}
                </div>
                """,
                    unsafe_allow_html=True
                )
            elif sugerencia['tipo'] == 'oferta_fin_semana':
                st.markdown(
                    f"""
                <div class="savings-alert">
                    {sugerencia['mensaje']}
                </div>
                """,
                    unsafe_allow_html=True
                )
    
    st.markdown("---")
    
    # =========================
    # MOSTRAR RECOMENDACIONES (agrego badges y explicación)
    # =========================
    st.markdown("### 🏆 Tus Mejores Opciones")
    for idx, (_, viaje) in enumerate(df_final.iterrows()):
        match_class, match_text = get_match_level(viaje['score'])
        badges = []
        if viaje['score'] >= 85:
            badges.append('🎯 Coincidencia Perfecta')
        elif viaje['score'] >= 70:
            badges.append('✅ Muy Buena Opción')
        elif viaje['score'] >= 50:
            badges.append('⚡ Opción Viable')
        if viaje['precio_min'] <= user_preferences['presupuesto_max']:
            badges.append('💸 Dentro de tu presupuesto')
        if user_preferences['clima_preferido'] != 'Sin preferencia' and viaje['categoria_clima'] == user_preferences['clima_preferido']:
            badges.append('🌤️ Clima preferido')
        if viaje['asientos_disponibles'] >= 30:
            badges.append('🟢 Alta disponibilidad')
        elif viaje['asientos_disponibles'] >= 15:
            badges.append('🟡 Disponibilidad media')
        else:
            badges.append('🔴 Pocos asientos')
        explicacion = ', '.join(badges)
        # Card con imagen y datos
        st.markdown(f"""
        <div class="recommendation-card" style="display:flex; align-items:stretch; background:#fff; border-radius:18px; box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:1.2rem; overflow:hidden;">
            {f'<img src="{viaje["url_imagen_destino"]}" alt="{viaje["destino"]}" style="width:160px; height:100%; object-fit:cover; background:#eee;">' if pd.notna(viaje.get('url_imagen_destino')) else ''}
            <div style="flex:1; padding:1.2rem 1.5rem; display:flex; flex-direction:column; justify-content:center;">
                <div style="background:#28a745; color:#fff; border-radius:12px 12px 0 0; padding:0.4rem 1rem; font-weight:600; font-size:1.05rem; margin-bottom:0.7rem;">
                    {' | '.join(badges)}
                </div>
                <div style="font-size:1.25rem; font-weight:700; color:#004E89; margin-bottom:0.2rem;">{viaje['destino']} <span style='font-size:1rem; color:#888;'>con {viaje['empresa']}</span></div>
                <div style="font-size:1.05rem; color:#222; margin-bottom:0.3rem;">Precio: <b>S/ {viaje['precio_min']}</b> | Fecha: {viaje['fecha_viaje'].strftime('%d/%m/%Y')} | Rating: {viaje['rating_empresa']}⭐</div>
                <div style="font-size:0.98rem; color:#555; margin-bottom:0.2rem;">Clima: {viaje['categoria_clima']} | Asientos: {viaje['asientos_disponibles']}</div>
                <div style="font-size:0.95rem; color:#888;">Motivo: {explicacion}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Controles de paginación inferior
    if total_paginas > 1:
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        with col_nav1:
            if st.button("⬅️ Anterior", key="prev_bottom", disabled=st.session_state.pagina_actual == 1):
                st.session_state.pagina_actual -= 1
                st.rerun()
        with col_nav2:
            st.markdown(
                f"<div style='text-align:center; padding:0.5rem; font-weight:600;'>Página {st.session_state.pagina_actual} de {total_paginas}</div>",
                unsafe_allow_html=True
            )
        with col_nav3:
            if st.button("Siguiente ➡️", key="next_bottom", disabled=st.session_state.pagina_actual == total_paginas):
                st.session_state.pagina_actual += 1
                st.rerun()

    # =========================
    # MAPA DE DESTINOS
    # =========================
    st.markdown("---")
    st.markdown("### 🗺️ Ubicación de Destinos Recomendados")
    
    COORDENADAS_DESTINOS = {
        "Arequipa": (-16.4090, -71.5375),
        "Trujillo": (-8.1159, -79.0299),
        "Cusco": (-13.5319, -71.9675),
        "Piura": (-5.1945, -80.6328),
        "Huancayo": (-12.0651, -75.2049),
        "Huaraz": (-9.5278, -77.5278),
    }
    
    # Crear mapa centrado en Perú
    m = folium.Map(location=[-9.19, -75.0152], zoom_start=6, tiles='CartoDB positron')
    
    # Agregar marcadores para cada destino recomendado
    destinos_agregados = set()
    for _, row in df_final.iterrows():
        destino = row['destino']
        
        # Evitar duplicados
        if destino in destinos_agregados or destino not in COORDENADAS_DESTINOS:
            continue
            
        destinos_agregados.add(destino)
        lat, lon = COORDENADAS_DESTINOS[destino]
        
        # Determinar color según ranking
        ranking = df_final[df_final['destino'] == destino]['score'].max()
        if ranking >= 90:
            icon_color = 'gold'
            icon_text = '🥇'
        elif ranking >= 80:
            icon_color = 'silver'
            icon_text = '🥈'
        elif ranking >= 70:
            icon_color = 'orange'
            icon_text = '🥉'
        else:
            icon_color = 'blue'
            icon_text = '📍'
        
        # Obtener el mejor viaje para este destino
        mejor_viaje = df_final[df_final['destino'] == destino].iloc[0]
        
        # Crear popup con información
        popup_html = f"""
        <div style='min-width:250px;'>
            <h4 style='color:#FF6B35;'>{destino}</h4>
            <p><b>Mejor opción:</b> {mejor_viaje['empresa']}</p>
            <p><b>Precio:</b> S/ {mejor_viaje['precio_min']:.0f}</p>
            <p><b>Fecha:</b> {mejor_viaje['fecha_viaje'].strftime('%d/%m/%Y')}</p>
            <p><b>Puntuación:</b> {mejor_viaje['score']:.1f}/100</p>
        </div>
        """
        
        # Crear marcador
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background-color: {icon_color};
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    border: 2px solid white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                ">
                    {icon_text}
                </div>
                """
            )
        ).add_to(m)
    
    # Mostrar mapa en Streamlit
    with st.container():
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st_folium(m, width=1200, height=500)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Manejo de caso sin resultados
    st.markdown(
        """
        <div class="no-results">
            <h3>😔 No encontramos recomendaciones que coincidan con tus criterios</h3>
            <p>Intenta ajustar tus preferencias en la barra lateral o aumentar tu presupuesto.</p>
            <p>También puedes intentar ser más flexible con las fechas de viaje.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image("https://i.imgur.com/6NKPrhO.png", width=300, use_column_width=False)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding:1rem; color:var(--medium-gray);">
        ChaskiWay © 2023 - Buscador Inteligente de Viajes
    </div>
    """,
    unsafe_allow_html=True
)