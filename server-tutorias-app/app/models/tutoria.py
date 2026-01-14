"""
Modelo de base de datos para la entidad Tutoría.

Define la estructura de la tabla de tutorías en el sistema, incluyendo
relaciones con alumnos y tutores, estados de progreso y campos de seguimiento.
"""

from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, Text, ForeignKey, Column
from datetime import datetime, timezone
from enum import Enum

if TYPE_CHECKING:
    from app.models.alumno import Alumno
    from app.models.tutor import Tutor


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class EstadoTutoria(str, Enum):
    """
    Estados posibles de una tutoría.
    
    PENDIENTE: La tutoría ha sido asignada pero no ha iniciado.
    EN_CURSO: La tutoría está actualmente en progreso.
    COMPLETADA: La tutoría ha sido finalizada.
    """
    PENDIENTE = "pendiente"
    EN_CURSO = "en curso"
    COMPLETADA = "completada"


class Tutoria(SQLModel, table=True):
    """
    Representa una sesión de tutoría entre un alumno y un tutor.
    
    Attributes:
        id_tutoria: Identificador único de la tutoría.
        alumno_id: ID del alumno asignado (obligatorio).
        tutor_id: ID del tutor asignado (opcional, puede ser NULL).
        periodo: Periodo académico de la tutoría (ej. "Enero-Junio 2025").
        observaciones: Notas o comentarios sobre la tutoría.
        estado: Estado actual de la tutoría.
        semestre: Semestre académico del alumno durante esta tutoría.
        reporte_integral_guardado: Indica si el reporte integral ha sido guardado.
        created_at: Fecha y hora de creación del registro.
        updated_at: Fecha y hora de última actualización del registro.
        alumno: Relación con el modelo Alumno.
        tutor: Relación con el modelo Tutor.
    """
    
    id_tutoria: Optional[int] = Field(default=None, primary_key=True)
    
    alumno_id: int = Field(
        sa_column=Column("alumno_id", ForeignKey("alumno.id_alumno", ondelete="CASCADE"), index=True)
    )
    
    tutor_id: Optional[int] = Field(
        default=None,
        sa_column=Column("tutor_id", ForeignKey("tutor.id_tutor", ondelete="SET NULL"), index=True)
    )
    
    periodo: Optional[str] = Field(default=None, max_length=100, index=True)
    observaciones: Optional[str] = Field(default=None, sa_column=Column(Text))
    estado: EstadoTutoria = Field(default=EstadoTutoria.PENDIENTE)
    semestre: int = Field(ge=1, le=14)
    reporte_integral_guardado: bool = Field(default=False, nullable=False)
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type:ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type:ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
    
    alumno: Optional["Alumno"] = Relationship(back_populates="tutorias")
    tutor: Optional["Tutor"] = Relationship(back_populates="tutorias")
