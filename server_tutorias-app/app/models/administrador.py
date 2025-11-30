"""
Modelo de base de datos para la entidad Administrador.

Define la estructura de la tabla de administradores del sistema,
incluyendo credenciales de autenticación y metadatos de registro.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime, timezone
from enum import Enum


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


# 1. Definimos los Roles posibles como un Enum
class RolAdministrador(str, Enum):
    SUPER_ADMIN = "super_admin"
    PSICOLOGIA = "psicologia"
    CIENCIAS_BASICAS = "ciencias_basicas"
    JEFATURA_ACADEMICA = "jefatura_academica"


class Administrador(SQLModel, table=True):
    """
    Representa a un administrador del sistema de gestión de tutorías.
    
    Los administradores tienen acceso completo a todas las funcionalidades
    del sistema, incluyendo gestión de usuarios y configuraciones.
    
    Attributes:
        id_admin: Identificador único del administrador.
        usuario: Nombre de usuario único para autenticación.
        contraseña: Hash de la contraseña del administrador.
        rol: Rol que define los permisos del administrador (Nuevo campo).
        created_at: Fecha y hora de creación del registro.
        updated_at: Fecha y hora de última actualización del registro.
    """
    
    id_admin: Optional[int] = Field(default=None, primary_key=True)
    usuario: str = Field(max_length=100, unique=True, index=True)
    contraseña: str
    
    # 2. Agregamos el campo rol
    # Por defecto será SUPER_ADMIN para mantener compatibilidad con los existentes
    rol: RolAdministrador = Field(default=RolAdministrador.SUPER_ADMIN)
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )