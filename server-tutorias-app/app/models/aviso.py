"""
Modelo de base de datos para la entidad Aviso.

Define la estructura de la tabla de avisos que los administradores
pueden crear y publicar para comunicar información a los alumnos.
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, Text
from typing import Optional
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Aviso(SQLModel, table=True):
    """
    Representa un aviso o anuncio del sistema de tutorías.
    
    Los avisos pueden ser creados por administradores y publicados
    para que los alumnos puedan verlos. Pueden incluir enlaces externos
    y pueden estar en estado borrador (inactivo) antes de ser publicados.
    
    Attributes:
        id: Identificador único del aviso.
        titulo: Título del aviso (indexado para búsquedas).
        descripcion: Contenido completo del aviso (tipo Text para textos largos).
        link: URL opcional a recurso externo relacionado.
        is_activo: Indica si el aviso está publicado (True) o en borrador (False).
        created_at: Fecha y hora de creación del aviso.
        updated_at: Fecha y hora de última actualización del aviso.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True, max_length=255)
    descripcion: str = Field(sa_column=Column(Text))
    link: Optional[str] = Field(default=None, max_length=1024)
    is_activo: bool = Field(default=False, nullable=False)
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type:ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type:ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
