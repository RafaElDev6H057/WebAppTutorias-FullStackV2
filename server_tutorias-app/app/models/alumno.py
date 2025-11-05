"""
Modelo de base de datos para la entidad Alumno.

Define la estructura de la tabla de alumnos en el sistema de gestión de tutorías,
incluyendo información académica y de contacto.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .tutoria import Tutoria


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Alumno(SQLModel, table=True):
    """
    Representa a un alumno registrado en el sistema de tutorías.
    
    Attributes:
        id_alumno: Identificador único del alumno.
        nombre: Nombre(s) del alumno.
        apellido_p: Apellido paterno.
        apellido_m: Apellido materno (opcional).
        num_control: Número de control único del alumno.
        contraseña: Hash de la contraseña del alumno.
        carrera: Nombre de la carrera que cursa.
        semestre_actual: Semestre actual del alumno (1-14).
        estado: Estado del alumno en el sistema (A=Activo por defecto).
        telefono: Número telefónico de contacto (opcional).
        correo: Dirección de correo electrónico.
        requires_password_change: Indica si el alumno debe cambiar su contraseña.
        created_at: Fecha y hora de creación del registro.
        updated_at: Fecha y hora de última actualización del registro.
        tutorias: Relación con las tutorías asignadas al alumno.
    """
    
    id_alumno: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido_p: str = Field(max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    num_control: str = Field(max_length=50, unique=True, index=True)
    contraseña: str
    carrera: str = Field(max_length=100)
    semestre_actual: int = Field(ge=1, le=14)
    estado: str = Field(default="A", max_length=50)
    telefono: Optional[str] = Field(default=None, max_length=100)
    correo: str = Field(max_length=255, index=True)
    requires_password_change: bool = Field(default=True)
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), # type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), # type: ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
    
    tutorias: List["Tutoria"] = Relationship(back_populates="alumno")
