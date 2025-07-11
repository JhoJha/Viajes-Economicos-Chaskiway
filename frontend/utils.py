# frontend/utils.py
"""
Utilidades para el frontend de Chaskiway
- Verificación de dependencias
- Validación de datos
- Funciones auxiliares
"""

import streamlit as st
import sys
from pathlib import Path

def check_dependencies():
    """
    Verifica que todas las dependencias necesarias estén instaladas.
    """
    missing_deps = []
    
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    try:
        import streamlit
    except ImportError:
        missing_deps.append("streamlit")
    
    try:
        import sqlite3
    except ImportError:
        missing_deps.append("sqlite3")
    
    try:
        import folium
    except ImportError:
        missing_deps.append("folium")
    
    try:
        from streamlit_folium import st_folium
    except ImportError:
        missing_deps.append("streamlit_folium")
    
    try:
        import plotly
    except ImportError:
        missing_deps.append("plotly")
    
    if missing_deps:
        st.error(f"❌ Faltan dependencias: {', '.join(missing_deps)}")
        st.info("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_database_exists():
    """
    Verifica que la base de datos exista y sea accesible.
    """
    db_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "viajes_grupales.db"
    
    if not db_path.exists():
        st.error("❌ Base de datos no encontrada")
        st.info("💡 Ejecuta primero: python main.py")
        return False
    
    return True

def format_price(price):
    """
    Formatea un precio de manera consistente.
    """
    try:
        return f"S/ {float(price):.0f}"
    except (ValueError, TypeError):
        return "S/ --"

def format_date(date_obj):
    """
    Formatea una fecha de manera consistente.
    """
    try:
        return date_obj.strftime('%d/%m/%Y')
    except AttributeError:
        return "Fecha no disponible"

def get_emoji_for_climate(climate):
    """
    Retorna el emoji apropiado para cada tipo de clima.
    """
    climate_emojis = {
        "Cálido": "🌞",
        "Templado": "🌤️", 
        "Frío": "❄️"
    }
    return climate_emojis.get(climate, "🌡️")

def get_emoji_for_rating(rating):
    """
    Retorna el emoji apropiado para cada rating.
    """
    try:
        rating_float = float(rating)
        if rating_float >= 4.5:
            return "⭐⭐⭐⭐⭐"
        elif rating_float >= 4.0:
            return "⭐⭐⭐⭐"
        elif rating_float >= 3.0:
            return "⭐⭐⭐"
        elif rating_float >= 2.0:
            return "⭐⭐"
        else:
            return "⭐"
    except (ValueError, TypeError):
        return "⭐"

def validate_user_input(presupuesto, fecha, clima):
    """
    Valida los inputs del usuario.
    """
    errors = []
    
    if not presupuesto or presupuesto <= 0:
        errors.append("💰 El presupuesto debe ser mayor a 0")
    
    if not fecha:
        errors.append("📅 Debes seleccionar una fecha de viaje")
    
    if not clima or clima == "Sin preferencia":
        errors.append("🌡️ Debes seleccionar un tipo de clima")
    
    return errors

def show_loading_message():
    """
    Muestra un mensaje de carga atractivo.
    """
    st.markdown("""
    <div style="text-align:center; padding:2rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">🚌</div>
        <h3>Buscando las mejores opciones para ti...</h3>
        <p>Nuestro algoritmo está analizando miles de opciones</p>
    </div>
    """, unsafe_allow_html=True)

def show_no_results_message():
    """
    Muestra un mensaje cuando no hay resultados.
    """
    st.markdown("""
    <div style="text-align:center; padding:3rem; background:#f8f9fa; border-radius:15px;">
        <div style="font-size:4rem; margin-bottom:1rem;">😔</div>
        <h3>No encontramos opciones que coincidan</h3>
        <p>Intenta ajustar tus criterios de búsqueda:</p>
        <ul style="text-align:left; display:inline-block;">
            <li>Aumenta tu presupuesto</li>
            <li>Se más flexible con las fechas</li>
            <li>Cambia el tipo de clima</li>
            <li>Selecciona otro destino</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_error_boundary(func):
    """
    Decorador para manejar errores en funciones del frontend.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.info("💡 Si el problema persiste, contacta al equipo de desarrollo")
            return None
    return wrapper 