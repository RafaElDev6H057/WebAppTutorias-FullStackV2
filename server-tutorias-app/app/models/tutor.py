"""
Modelo de base de datos para la entidad Tutor.

Define la estructura de la tabla de tutores en el sistema de gestión de tutorías,
incluyendo información personal y de autenticación.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.tutoria import Tutoria


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Tutor(SQLModel, table=True):
    """
    Representa a un tutor registrado en el sistema de tutorías.
    
    Attributes:
        id_tutor: Identificador único del tutor.
        nombre: Nombre(s) del tutor.
        apellido_p: Apellido paterno.
        apellido_m: Apellido materno (opcional).
        correo: Dirección de correo electrónico única.
        contraseña: Hash de la contraseña del tutor.
        requires_password_change: Indica si el tutor debe cambiar su contraseña.
        created_at: Fecha y hora de creación del registro.
        updated_at: Fecha y hora de última actualización del registro.
        tutorias: Relación con las tutorías asignadas al tutor.
    """
    
    id_tutor: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido_p: str = Field(max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: str = Field(index=True, unique=True, max_length=255)
    contraseña: str
    requires_password_change: bool = Field(default=True)
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type:ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
    
    tutorias: List["Tutoria"] = Relationship(back_populates="tutor")
