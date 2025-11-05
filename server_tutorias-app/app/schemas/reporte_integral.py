"""
Esquemas Pydantic para validación y serialización de datos de Reporte Integral.

Define los diferentes esquemas utilizados en las operaciones CRUD de reportes
integrales de tutorías, con validaciones numéricas y de texto.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ReporteIntegralBase(BaseModel):
    """
    Esquema base con los campos comunes de Reporte Integral.
    
    Incluye validaciones de valores no negativos para campos numéricos
    y longitudes máximas para campos de texto.
    """
    
    tutoria_grupal: int = Field(ge=0, default=0)
    tutoria_individual: int = Field(ge=0, default=0)
    seguimiento_1: Optional[str] = None
    seguimiento_2: Optional[str] = None
    seguimiento_3: Optional[str] = None
    jefatura_academica: int = Field(ge=0, default=0)
    ciencias_basicas: int = Field(ge=0, default=0)
    psicologia: int = Field(ge=0, default=0)
    materias_aprobadas: int = Field(ge=0, default=0)
    materias_no_aprobadas: Optional[str] = None


class ReporteIntegralCreate(ReporteIntegralBase):
    """
    Esquema para la creación de un nuevo reporte integral.
    
    Requiere especificar la tutoría asociada mediante su ID.
    """
    
    id_tutoria: int


class ReporteIntegralRead(ReporteIntegralBase):
    """
    Esquema para lectura de datos de reporte integral.
    
    Incluye los identificadores del reporte y de la tutoría asociada.
    """
    
    id: int
    id_tutoria: int
    
    model_config = ConfigDict(from_attributes=True)


class ReporteIntegralUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un reporte integral.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    No permite cambiar la tutoría asociada (id_tutoria no incluido).
    """
    
    tutoria_grupal: Optional[int] = Field(default=None, ge=0)
    tutoria_individual: Optional[int] = Field(default=None, ge=0)
    seguimiento_1: Optional[str] = None
    seguimiento_2: Optional[str] = None
    seguimiento_3: Optional[str] = None
    jefatura_academica: Optional[int] = Field(default=None, ge=0)
    ciencias_basicas: Optional[int] = Field(default=None, ge=0)
    psicologia: Optional[int] = Field(default=None, ge=0)
    materias_aprobadas: Optional[int] = Field(default=None, ge=0)
    materias_no_aprobadas: Optional[str] = None
