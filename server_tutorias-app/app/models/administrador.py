"""
Modelo de base de datos para la entidad Administrador.

Define la estructura de la tabla de administradores del sistema,
incluyendo credenciales de autenticación y metadatos de registro.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Administrador(SQLModel, table=True):
    """
    Representa a un administrador del sistema de gestión de tutorías.
    
    Los administradores tienen acceso completo a todas las funcionalidades
    del sistema, incluyendo gestión de usuarios y configuraciones.
    
    Attributes:
        id_admin: Identificador único del administrador.
        usuario: Nombre de usuario único para autenticación.
        contraseña: Hash de la contraseña del administrador.
        created_at: Fecha y hora de creación del registro.
        updated_at: Fecha y hora de última actualización del registro.
    """
    
    id_admin: Optional[int] = Field(default=None, primary_key=True)
    usuario: str = Field(max_length=100, unique=True, index=True)
    contraseña: str
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
