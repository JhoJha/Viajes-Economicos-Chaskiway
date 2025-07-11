#!/usr/bin/env python3
"""
Script de configuración para Chaskiway
- Instala dependencias
- Verifica configuración
- Crea directorios necesarios
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

def run_command(command, description):
    """Ejecuta un comando y maneja errores."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida de error: {e.stderr}")
        return False

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} no es compatible. Se requiere Python 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} es compatible")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto."""
    print("📦 Instalando dependencias...")
    
    # Verificar si pip está disponible
    if not shutil.which("pip"):
        print("❌ pip no está disponible. Instala pip primero.")
        return False
    
    # Instalar dependencias
    success = run_command("pip install -r requirements.txt", "Instalando dependencias")
    return success

def create_directories():
    """Crea los directorios necesarios para el proyecto."""
    print("📁 Creando directorios...")
    
    directories = [
        "data/raw/redbus",
        "data/raw/clima", 
        "data/raw/imagenes",
        "data/processed",
        "logs/scrapers",
        "logs/app",
        "logs/database"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def check_env_file():
    """Verifica si existe el archivo .env y da instrucciones."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Archivo .env no encontrado")
        print("📝 Crea un archivo .env con las siguientes variables:")
        print("""
# .env
VISUAL_CROSSING_API_KEY=tu_api_key_aqui
PIXABAY_API_KEY=tu_api_key_aqui
        """)
        print("📖 Consulta docs/API_KEYS.md para más información")
        return False
    else:
        print("✅ Archivo .env encontrado")
        return True

def test_imports():
    """Prueba que las importaciones principales funcionen."""
    print("🧪 Probando importaciones...")
    
    try:
        import streamlit
        import pandas
        import sqlite3
        import requests
        print("✅ Importaciones básicas funcionando")
        
        # Probar plotly si está instalado
        try:
            import plotly
            print("✅ Plotly disponible para gráficos")
        except ImportError:
            print("⚠️  Plotly no está instalado. Los gráficos del dashboard no funcionarán")
        
        return True
    except ImportError as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def main():
    """Función principal del script de configuración."""
    print("🚀 Configurando Chaskiway...")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Fallo en la instalación de dependencias")
        sys.exit(1)
    
    # Probar importaciones
    if not test_imports():
        print("❌ Fallo en las importaciones")
        sys.exit(1)
    
    # Verificar archivo .env
    check_env_file()
    
    print("=" * 50)
    print("🎉 Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Configura tus API keys en el archivo .env")
    print("2. Ejecuta 'python main.py' para procesar datos")
    print("3. Ejecuta 'streamlit run frontend/app.py' para iniciar la app")
    print("\n📖 Consulta el README.md para más información")

if __name__ == "__main__":
    main() 