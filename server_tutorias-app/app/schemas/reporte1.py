"""
Esquemas Pydantic para validación y serialización de datos de Reporte1.

Define los diferentes esquemas utilizados en las operaciones CRUD de reportes
de proyectos de tutores, con validaciones de porcentaje y campos de texto.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class Reporte1Base(BaseModel):
    """
    Esquema base con los campos comunes de Reporte1.
    
    Incluye validaciones de longitud para campos de texto y
    validación de rango para el porcentaje de avance (0-100).
    """
    
    nombre_tutor: str = Field(max_length=300)
    periodo: str = Field(max_length=100)
    nombre_proyecto: str = Field(max_length=500)
    porcentaje_avance: float = Field(ge=0, le=100)
    objetivo: str
    descripcion: str
    metas: str
    actividades: str
    documentos_anexados: Optional[str] = None
    conclusiones: str
    observaciones: str


class Reporte1Create(Reporte1Base):
    """
    Esquema para la creación de un nuevo Reporte1.
    
    El id_tutor no se incluye en el esquema ya que se obtiene
    automáticamente del token JWT del usuario autenticado.
    """
    
    pass


class Reporte1Update(BaseModel):
    """
    Esquema para la actualización parcial de un Reporte1.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    nombre_tutor: Optional[str] = Field(default=None, max_length=300)
    periodo: Optional[str] = Field(default=None, max_length=100)
    nombre_proyecto: Optional[str] = Field(default=None, max_length=500)
    porcentaje_avance: Optional[float] = Field(default=None, ge=0, le=100)
    objetivo: Optional[str] = None
    descripcion: Optional[str] = None
    metas: Optional[str] = None
    actividades: Optional[str] = None
    documentos_anexados: Optional[str] = None
    conclusiones: Optional[str] = None
    observaciones: Optional[str] = None


class Reporte1Read(Reporte1Base):
    """
    Esquema para lectura de datos de Reporte1.
    
    Incluye los identificadores del reporte y del tutor creador,
    además de los timestamps de creación y actualización.
    """
    
    id: int
    id_tutor: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
