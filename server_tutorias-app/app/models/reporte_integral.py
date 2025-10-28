# app/models/reporte_integral.py

from sqlmodel import SQLModel, Field, Relationship # Añadido Relationship
from typing import Optional, TYPE_CHECKING # Añadido TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey # Añadido ForeignKey

# Para la relación (opcional pero recomendado)
if TYPE_CHECKING:
    from app.models.tutoria import Tutoria

class ReporteIntegral(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- NUEVA CLAVE FORÁNEA ---
    id_tutoria: int = Field(foreign_key="tutoria.id_tutoria", index=True)
    # ---------------------------

    # --- Campos del formulario (sin cambios) ---
    tutoria_grupal: int = Field(default=0)
    tutoria_individual: int = Field(default=0)
    seguimiento_1: Optional[str] = Field(default=None, max_length=500)
    seguimiento_2: Optional[str] = Field(default=None, max_length=500)
    seguimiento_3: Optional[str] = Field(default=None, max_length=500)
    jefatura_academica: int = Field(default=0)
    ciencias_basicas: int = Field(default=0)
    psicologia: int = Field(default=0)
    materias_aprobadas: int = Field(default=0)
    materias_no_aprobadas: Optional[str] = Field(default=None, max_length=500)

    # --- Timestamps (sin cambios) ---
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

    # --- Relación Inversa (Opcional pero útil) ---
    # Permite acceder a la tutoría desde el reporte si lo necesitas
    # tutoria: Optional["Tutoria"] = Relationship(back_populates="reportes_integrales")
    # Nota: Si añades esto, también debes añadir 'reportes_integrales: List["ReporteIntegral"] = Relationship(back_populates="tutoria")' en models/tutoria.py