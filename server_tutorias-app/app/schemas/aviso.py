"""
Esquemas Pydantic para validación y serialización de datos de Aviso.

Define los diferentes esquemas utilizados en las operaciones CRUD de avisos
que los administradores pueden publicar para los alumnos.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AvisoBase(BaseModel):
    """
    Esquema base con los campos comunes de Aviso.
    
    Incluye validaciones de longitud para título y descripción.
    """
    
    titulo: str = Field(min_length=3, max_length=255)
    descripcion: str
    link: Optional[str] = Field(default=None, max_length=1024)
    is_activo: bool = False


class AvisoCreate(AvisoBase):
    """
    Esquema para la creación de un nuevo aviso.
    
    Por defecto, los avisos nuevos se crean en estado inactivo (borrador)
    hasta que el administrador decida publicarlos.
    """
    
    pass


class AvisoUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un aviso.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    titulo: Optional[str] = Field(default=None, min_length=3, max_length=255)
    descripcion: Optional[str] = None
    link: Optional[str] = Field(default=None, max_length=1024)
    is_activo: Optional[bool] = None


class AvisoRead(AvisoBase):
    """
    Esquema para lectura de datos de aviso.
    
    Incluye el identificador y los timestamps de creación y actualización.
    """
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
