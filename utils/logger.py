# utils/logger.py
"""
Sistema de logging centralizado para Chaskiway
- Configuración unificada de logging
- Diferentes niveles para desarrollo y producción
- Rotación de archivos de log
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import os

def setup_logger(name="chaskiway", level=logging.INFO, log_file=None):
    """
    Configura un logger centralizado para el proyecto.
    
    Args:
        name (str): Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str): Ruta del archivo de log (opcional)
    
    Returns:
        logging.Logger: Logger configurado
    """
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (si se especifica)
    if log_file:
        # Crear directorio de logs si no existe
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_scraper_logger(scraper_name):
    """
    Obtiene un logger específico para scrapers.
    
    Args:
        scraper_name (str): Nombre del scraper (redbus, clima, imagenes)
    
    Returns:
        logging.Logger: Logger configurado para el scraper
    """
    log_file = f"logs/scrapers/{scraper_name}_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger(f"scraper.{scraper_name}", log_file=log_file)

def get_app_logger():
    """
    Obtiene un logger específico para la aplicación Streamlit.
    
    Returns:
        logging.Logger: Logger configurado para la app
    """
    log_file = f"logs/app/streamlit_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger("app.streamlit", log_file=log_file)

def get_database_logger():
    """
    Obtiene un logger específico para operaciones de base de datos.
    
    Returns:
        logging.Logger: Logger configurado para la BD
    """
    log_file = f"logs/database/db_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger("database", log_file=log_file)

# Logger por defecto
logger = setup_logger()

if __name__ == "__main__":
    # Ejemplo de uso
    logger.info("Sistema de logging configurado correctamente")
    logger.warning("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error") 