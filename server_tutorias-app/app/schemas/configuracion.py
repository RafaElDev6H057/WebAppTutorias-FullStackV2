"""
Esquemas Pydantic para validación de configuración del sistema.

Define los esquemas para lectura y actualización de la configuración global,
con validación estricta de valores permitidos para la etapa de reporte integral.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class ConfiguracionRead(BaseModel):
    """
    Esquema para lectura de la configuración del sistema.
    
    Retorna el estado actual de las configuraciones globales.
    """
    
    reporte_integral_etapa: int
    
    model_config = ConfigDict(from_attributes=True)


class ConfiguracionUpdate(BaseModel):
    """
    Esquema para actualización de la configuración del sistema.
    
    Utiliza Literal para restringir los valores permitidos únicamente
    a las etapas válidas del reporte integral (1, 2 o 3).
    """
    
    reporte_integral_etapa: Literal[1, 2, 3]
