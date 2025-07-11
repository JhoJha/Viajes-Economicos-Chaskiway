# 🔑 Configuración de API Keys - Chaskiway

Este documento explica cómo configurar las API keys necesarias para el funcionamiento completo del proyecto.

## 📋 APIs Requeridas

### 1. SerpAPI (para imágenes de destinos)
**Propósito:** Obtener imágenes de los destinos usando Google Images vía SerpAPI
**URL:** https://serpapi.com/

#### Configuración:
1. Regístrate en SerpAPI y obtén tu API key gratuita.
2. Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
SERPAPI_KEY=tu_api_key_aqui
```

## 🔧 Configuración del Proyecto

### Paso 1: Instalar dependencias
```bash
pip install python-dotenv
```

### Paso 2: Crear archivo .env
```bash
# .env
SERPAPI_KEY=tu_api_key_serpapi
```

### Paso 3: El scraper de imágenes ya está configurado para usar la variable de entorno:

```python
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('SERPAPI_KEY')
```

## ⚠️ Notas Importantes

1. **Nunca subas el archivo `.env` a Git**
2. **El archivo `.env` ya está incluido en `.gitignore`**
3. **Las API keys gratuitas tienen límites de uso**
4. **Para producción, considera planes pagos**

## 🚀 Verificación

Para verificar que todo funciona:

1. Ejecuta el scraper de imágenes:
```bash
python backend/scraping/imagenes/scraper.py
```

2. Ejecuta el pipeline completo:
```bash
python main.py
```

## 📞 Soporte

- SerpAPI: https://serpapi.com/contact

## 🔒 Seguridad

- Nunca compartas tus API keys
- Usa variables de entorno en producción
- Revisa regularmente el uso de tus APIs
- Considera rotar las keys periódicamente 