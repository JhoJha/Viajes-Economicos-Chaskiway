# 🔑 Configuración de API Keys - Chaskiway

Este documento explica cómo configurar las API keys necesarias para el funcionamiento completo del proyecto.

## 📋 APIs Requeridas

### 1. Visual Crossing Weather API
**Propósito:** Obtener datos de clima para los destinos
**URL:** https://www.visualcrossing.com/weather-api

#### Configuración:
1. Regístrate en Visual Crossing Weather API
2. Obtén tu API key gratuita
3. Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
VISUAL_CROSSING_API_KEY=tu_api_key_aqui
```

### 2. Pixabay API
**Propósito:** Obtener imágenes de los destinos
**URL:** https://pixabay.com/api/docs/

#### Configuración:
1. Regístrate en Pixabay
2. Obtén tu API key gratuita
3. Agrega a tu archivo `.env`:

```bash
# .env
PIXABAY_API_KEY=tu_api_key_aqui
```

## 🔧 Configuración del Proyecto

### Paso 1: Instalar dependencias
```bash
pip install python-dotenv
```

### Paso 2: Crear archivo .env
```bash
# .env
VISUAL_CROSSING_API_KEY=tu_api_key_visual_crossing
PIXABAY_API_KEY=tu_api_key_pixabay
```

### Paso 3: Modificar los scrapers
Actualiza los archivos de scraping para usar las variables de entorno:

#### Para clima (backend/scraping/clima/scraper.py):
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('VISUAL_CROSSING_API_KEY')
```

#### Para imágenes (backend/scraping/imagenes/scraper.py):
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PIXABAY_API_KEY')
```

## ⚠️ Notas Importantes

1. **Nunca subas el archivo `.env` a Git**
2. **El archivo `.env` ya está incluido en `.gitignore`**
3. **Las API keys gratuitas tienen límites de uso**
4. **Para producción, considera planes pagos**

## 🚀 Verificación

Para verificar que todo funciona:

1. Ejecuta el scraper de clima:
```bash
python backend/scraping/clima/scraper.py
```

2. Ejecuta el scraper de imágenes:
```bash
python backend/scraping/imagenes/scraper.py
```

3. Ejecuta el pipeline completo:
```bash
python main.py
```

## 📞 Soporte

Si tienes problemas con las APIs:
- Visual Crossing: https://www.visualcrossing.com/support
- Pixabay: https://pixabay.com/service/contact/

## 🔒 Seguridad

- Nunca compartas tus API keys
- Usa variables de entorno en producción
- Revisa regularmente el uso de tus APIs
- Considera rotar las keys periódicamente 