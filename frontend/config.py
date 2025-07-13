# frontend/config.py
"""
Configuración del frontend de Chaskiway
- Configuraciones de rendimiento
- Límites y constantes
- Configuraciones de UI
"""

# Configuraciones de rendimiento
CACHE_TTL = 3600  # 1 hora en segundos
MAX_RESULTS_PER_PAGE = 10
MAX_TOTAL_RESULTS = 100

# Configuraciones de UI
PRIMARY_COLOR = "#FF6B35"
SECONDARY_COLOR = "#F7931E"
DARK_BLUE = "#004E89"
SUCCESS_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
INFO_COLOR = "#17a2b8"

# Configuraciones de validación
MIN_BUDGET = 10
MAX_BUDGET = 10000
MIN_RATING = 0.0
MAX_RATING = 5.0
MIN_SEATS = 1
MAX_SEATS = 100

# Configuraciones de fechas
DEFAULT_FLEXIBILITY_DAYS = 7
MAX_FLEXIBILITY_DAYS = 30

# Configuraciones de scoring
SCORING_WEIGHTS = {
    'price': 0.40,
    'date_flexibility': 0.25,
    'climate_preference': 0.20,
    'company_rating': 0.10,
    'seat_availability': 0.05
}

# Configuraciones de mapas
MAP_CENTER = [-9.19, -75.0152]  # Centro de Perú
MAP_ZOOM = 6
MAP_TILES = 'CartoDB positron'

# Configuraciones de destinos
DESTINOS_COORDENADAS = {
    "Arequipa": (-16.4090, -71.5375),
    "Trujillo": (-8.1159, -79.0299),
    "Cusco": (-13.5319, -71.9675),
    "Piura": (-5.1945, -80.6328),
    "Huancayo": (-12.0651, -75.2049),
    "Huaraz": (-9.5278, -77.5278),
}

# Configuraciones de clima
CLIMATE_EMOJIS = {
    "Cálido": "🌞",
    "Templado": "🌤️", 
    "Frío": "❄️"
}

# Configuraciones de rating
RATING_EMOJIS = {
    5.0: "⭐⭐⭐⭐⭐",
    4.5: "⭐⭐⭐⭐⭐",
    4.0: "⭐⭐⭐⭐",
    3.5: "⭐⭐⭐⭐",
    3.0: "⭐⭐⭐",
    2.5: "⭐⭐⭐",
    2.0: "⭐⭐",
    1.5: "⭐⭐",
    1.0: "⭐",
    0.5: "⭐",
    0.0: "⭐"
}

# Configuraciones de disponibilidad
AVAILABILITY_LEVELS = {
    'high': {'min': 20, 'class': 'high-availability', 'text': 'Alta Disponibilidad'},
    'medium': {'min': 10, 'class': 'medium-availability', 'text': 'Disponibilidad Media'},
    'low': {'min': 1, 'class': 'low-availability', 'text': 'Pocos Asientos'},
    'none': {'min': 0, 'class': 'no-availability', 'text': 'Sin Disponibilidad'}
}

# Configuraciones de mensajes
MESSAGES = {
    'loading': "🔄 Cargando datos y preparando recomendaciones...",
    'no_data': "❌ No se encontraron datos. Verifica el pipeline de ETL.",
    'no_results': "😔 No encontramos opciones que coincidan con tus criterios",
    'error_loading': "❌ Error al cargar datos",
    'success_search': "✅ Búsqueda configurada exitosamente",
    'validation_error': "❌ Completa los campos obligatorios"
}

# Configuraciones de desarrollo
DEBUG_MODE = False
SHOW_PERFORMANCE_METRICS = False
ENABLE_CACHING = True 