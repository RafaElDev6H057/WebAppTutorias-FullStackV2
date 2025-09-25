# app/models/reporte_integral.py

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

class ReporteIntegral(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- Campos del formulario ---
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

    # --- Timestamps ---
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