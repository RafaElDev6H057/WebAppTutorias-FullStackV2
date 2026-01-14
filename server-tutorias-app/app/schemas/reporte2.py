"""
Esquemas Pydantic para validación y serialización de datos de Reporte2 (Final).

Define los diferentes esquemas utilizados en las operaciones CRUD del segundo reporte,
enfocado en resultados finales y conclusiones.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class Reporte2Base(BaseModel):
    """
    Esquema base con los campos comunes de Reporte2.
    """
    
    nombre_tutor: str = Field(max_length=300)
    periodo: str = Field(max_length=100)
    nombre_proyecto: str = Field(max_length=500)
    porcentaje_avance: float = Field(ge=0, le=100, description="Porcentaje final alcanzado")
    objetivo: str
    descripcion: str
    metas: str
    actividades: str
    documentos_anexados: Optional[str] = None
    conclusiones: str
    observaciones: str


class Reporte2Create(Reporte2Base):
    """
    Esquema para la creación de un nuevo Reporte2.
    El id_tutor se inyecta desde el token.
    """
    pass


class Reporte2Update(BaseModel):
    """
    Esquema para la actualización parcial de un Reporte2.
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


class Reporte2Read(Reporte2Base):
    """
    Esquema para lectura de datos de Reporte2.
    """
    
    id: int
    id_tutor: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)