# utils/validators.py
"""
Utilidades de validación de datos para Chaskiway
- Validación de formatos de fecha
- Validación de precios
- Validación de destinos
- Limpieza de datos
"""

import pandas as pd
import re
from datetime import datetime
from typing import List, Dict, Any

def validate_date_format(date_str: str) -> bool:
    """
    Valida que una fecha esté en formato correcto.
    
    Args:
        date_str (str): String de fecha a validar
    
    Returns:
        bool: True si la fecha es válida
    """
    try:
        # Intentar diferentes formatos
        formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d']
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False
    except:
        return False

def validate_price(price: Any) -> bool:
    """
    Valida que un precio sea válido.
    
    Args:
        price: Precio a validar
    
    Returns:
        bool: True si el precio es válido
    """
    try:
        price_float = float(price)
        return price_float > 0 and price_float < 10000  # Rango razonable
    except (ValueError, TypeError):
        return False

def validate_destination(destination: str) -> bool:
    """
    Valida que un destino sea válido.
    
    Args:
        destination (str): Nombre del destino
    
    Returns:
        bool: True si el destino es válido
    """
    if not destination or not isinstance(destination, str):
        return False
    
    # Limpiar el destino
    clean_dest = destination.strip()
    if len(clean_dest) < 2 or len(clean_dest) > 50:
        return False
    
    # Verificar que no contenga caracteres extraños
    if re.search(r'[<>"\']', clean_dest):
        return False
    
    return True

def validate_rating(rating: Any) -> bool:
    """
    Valida que un rating sea válido.
    
    Args:
        rating: Rating a validar
    
    Returns:
        bool: True si el rating es válido
    """
    try:
        rating_float = float(rating)
        return 0 <= rating_float <= 5  # Rating de 0 a 5
    except (ValueError, TypeError):
        return False

def validate_seats(seats: Any) -> bool:
    """
    Valida que el número de asientos sea válido.
    
    Args:
        seats: Número de asientos a validar
    
    Returns:
        bool: True si el número de asientos es válido
    """
    try:
        seats_int = int(seats)
        return 0 <= seats_int <= 100  # Rango razonable
    except (ValueError, TypeError):
        return False

def clean_company_name(company: str) -> str:
    """
    Limpia el nombre de una empresa.
    
    Args:
        company (str): Nombre de la empresa
    
    Returns:
        str: Nombre limpio
    """
    if not company:
        return "Empresa Desconocida"
    
    # Limpiar caracteres extraños
    clean_company = re.sub(r'[<>"\']', '', company.strip())
    
    # Capitalizar correctamente
    clean_company = clean_company.title()
    
    return clean_company if clean_company else "Empresa Desconocida"

def validate_redbus_data(data: Dict[str, Any]) -> List[str]:
    """
    Valida los datos de RedBus.
    
    Args:
        data (dict): Datos de RedBus
    
    Returns:
        List[str]: Lista de errores encontrados
    """
    errors = []
    
    # Validar estructura básica
    if not isinstance(data, dict):
        errors.append("Datos no son un diccionario válido")
        return errors
    
    # Validar campos requeridos
    required_fields = ['parentSrcCityName', 'parentDstCityName', 'inventories']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo requerido faltante: {field}")
    
    # Validar inventario
    if 'inventories' in data and isinstance(data['inventories'], list):
        for i, inventory in enumerate(data['inventories']):
            if not isinstance(inventory, dict):
                errors.append(f"Inventario {i} no es un diccionario válido")
                continue
            
            # Validar campos del inventario
            inventory_fields = ['departureTime', 'travelsName', 'fareList', 'availableSeats']
            for field in inventory_fields:
                if field not in inventory:
                    errors.append(f"Campo faltante en inventario {i}: {field}")
    
    return errors

def validate_climate_data(data: Dict[str, Any]) -> List[str]:
    """
    Valida los datos de clima.
    
    Args:
        data (dict): Datos de clima
    
    Returns:
        List[str]: Lista de errores encontrados
    """
    errors = []
    
    if not isinstance(data, dict):
        errors.append("Datos de clima no son un diccionario válido")
        return errors
    
    # Validar campos requeridos
    required_fields = ['location', 'temperature', 'date']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo requerido faltante en clima: {field}")
    
    return errors

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia un DataFrame aplicando validaciones.
    
    Args:
        df (pd.DataFrame): DataFrame a limpiar
    
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    if df.empty:
        return df
    
    # Crear copia para no modificar el original
    df_clean = df.copy()
    
    # Limpiar destinos
    if 'destino' in df_clean.columns:
        df_clean['destino'] = df_clean['destino'].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        df_clean = df_clean[df_clean['destino'].apply(validate_destination)]
    
    # Limpiar empresas
    if 'empresa' in df_clean.columns:
        df_clean['empresa'] = df_clean['empresa'].apply(clean_company_name)
    
    # Validar precios
    if 'precio_min' in df_clean.columns:
        df_clean = df_clean[df_clean['precio_min'].apply(validate_price)]
    
    # Validar ratings
    if 'rating_empresa' in df_clean.columns:
        df_clean = df_clean[df_clean['rating_empresa'].apply(validate_rating)]
    
    # Validar asientos
    if 'asientos_disponibles' in df_clean.columns:
        df_clean = df_clean[df_clean['asientos_disponibles'].apply(validate_seats)]
    
    # Validar fechas
    if 'fecha_viaje' in df_clean.columns:
        df_clean = df_clean[df_clean['fecha_viaje'].apply(validate_date_format)]
    
    return df_clean

def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Genera un reporte de calidad de datos.
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
    
    Returns:
        Dict[str, Any]: Reporte de calidad
    """
    report = {
        'total_rows': len(df),
        'missing_values': {},
        'data_types': {},
        'unique_values': {},
        'value_ranges': {}
    }
    
    if df.empty:
        return report
    
    # Análisis de valores faltantes
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            report['missing_values'][col] = {
                'count': missing_count,
                'percentage': (missing_count / len(df)) * 100
            }
    
    # Análisis de tipos de datos
    for col in df.columns:
        report['data_types'][col] = str(df[col].dtype)
    
    # Análisis de valores únicos
    for col in df.columns:
        unique_count = df[col].nunique()
        report['unique_values'][col] = unique_count
    
    # Análisis de rangos para columnas numéricas
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        report['value_ranges'][col] = {
            'min': df[col].min(),
            'max': df[col].max(),
            'mean': df[col].mean(),
            'median': df[col].median()
        }
    
    return report 