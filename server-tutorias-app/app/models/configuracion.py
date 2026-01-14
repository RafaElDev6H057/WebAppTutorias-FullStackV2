"""
Modelo de base de datos para la configuración del sistema.

Define una tabla singleton que almacena la configuración global del sistema,
específicamente la etapa actual del proceso de reporte integral de tutorías.
"""

from sqlmodel import SQLModel, Field
from typing import Optional


class ConfiguracionSistema(SQLModel, table=True):
    """
    Representa la configuración global del sistema de tutorías.
    
    Esta tabla está diseñada como singleton (un único registro con ID=1)
    para almacenar configuraciones que afectan a todo el sistema.
    
    Atributos de reporte integral:
        - Etapa 1: Solo permite llenar Seguimiento 1
        - Etapa 2: Permite llenar Seguimiento 1 y Seguimiento 2
        - Etapa 3: Reporte completo (todas las secciones habilitadas)
    
    Attributes:
        id: Identificador fijo (siempre 1) para garantizar registro único.
        reporte_integral_etapa: Etapa actual del proceso de reporte integral (1, 2 o 3).
    """
    
    id: Optional[int] = Field(default=1, primary_key=True)
    reporte_integral_etapa: int = Field(default=1, nullable=False)
