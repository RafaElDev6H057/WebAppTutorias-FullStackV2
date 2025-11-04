# app/schemas/reporte1.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime # Para el schema Read

# --- Esquema Base ---
# Contiene los campos que el tutor enviará
class Reporte1Base(BaseModel):
    nombre_tutor: str = Field(max_length=300)
    periodo: str = Field(max_length=100)
    nombre_proyecto: str = Field(max_length=500)
    porcentaje_avance: float = Field(ge=0, le=100) # Validamos que sea un porcentaje
    objetivo: str
    descripcion: str
    metas: str
    actividades: str
    documentos_anexados: Optional[str] = None
    conclusiones: str
    observaciones: str

# --- Esquema para Crear ---
# El 'id_tutor' no se pide en el JSON, se tomará del token
class Reporte1Create(Reporte1Base):
    pass

# --- Esquema para Actualizar ---
# Todos los campos son opcionales
class Reporte1Update(BaseModel):
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

# --- Esquema para Leer ---
# Devuelve los datos del reporte MÁS los IDs y timestamps
class Reporte1Read(Reporte1Base):
    id: int # ID del propio reporte
    id_tutor: int # ID del tutor que lo creó
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Permite crear desde el modelo ORM