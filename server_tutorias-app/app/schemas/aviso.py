# app/schemas/aviso.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Esquema Base ---
# Campos comunes que se usan para crear y leer
class AvisoBase(BaseModel):
    titulo: str = Field(min_length=3, max_length=255)
    descripcion: str
    link: Optional[str] = Field(default=None, max_length=1024)
    is_activo: bool = False # Por defecto, un aviso nuevo es un borrador

# --- Esquema para Crear ---
# Lo que el admin envía para crear un aviso nuevo
class AvisoCreate(AvisoBase):
    pass # Hereda todos los campos de AvisoBase

# --- Esquema para Actualizar ---
# Lo que el admin envía para modificar un aviso (todo opcional)
class AvisoUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3, max_length=255)
    descripcion: Optional[str] = None
    link: Optional[str] = Field(default=None, max_length=1024)
    is_activo: Optional[bool] = None

# --- Esquema para Leer ---
# Lo que la API devuelve (al admin o al alumno)
class AvisoRead(AvisoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Para convertir el modelo a esquema