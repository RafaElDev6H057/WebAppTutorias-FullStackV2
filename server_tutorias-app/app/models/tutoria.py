# app/models/tutoria.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone # Quitamos 'time'
from enum import Enum
from sqlalchemy import Column, DateTime, Text, ForeignKey

if TYPE_CHECKING:
    from app.models.alumno import Alumno
    from app.models.tutor import Tutor

# --- Enums ---
class EstadoTutoria(str, Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en curso"
    COMPLETADA = "completada"

# ❗ DiaSemana Enum eliminado

# --- Modelo Principal ---
class Tutoria(SQLModel, table=True):

    id_tutoria: Optional[int] = Field(default=None, primary_key=True)

    alumno_id: int = Field(
        sa_column=Column("alumno_id", ForeignKey("alumno.id_alumno", ondelete="CASCADE"), index=True)
    )
    
    # ✅ Corregido: ondelete="SET NULL"
    tutor_id: Optional[int] = Field(
        default=None,
        sa_column=Column("tutor_id", ForeignKey("tutor.id_tutor", ondelete="SET NULL"), index=True)
    )

    periodo: Optional[str] = Field(default=None, max_length=100, index=True) # Añadido index a periodo
    observaciones: Optional[str] = Field(default=None, sa_column=Column(Text))
    estado: EstadoTutoria = Field(default=EstadoTutoria.PENDIENTE)
    semestre: int = Field(ge=1, le=14) # Semestre del alumno en este periodo

    # ❗ Campos eliminados: es_activa, dia, hora

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )

    # Relaciones (sin cambios)
    alumno: Optional["Alumno"] = Relationship(back_populates="tutorias")
    tutor: Optional["Tutor"] = Relationship(back_populates="tutorias")