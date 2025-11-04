# app/models/reporte1.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Text, ForeignKey, Float

# Para la relación
if TYPE_CHECKING:
    from app.models.tutor import Tutor

class Reporte1(SQLModel, table=True):
    # --- Campos de Identificación ---
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Clave foránea para saber qué tutor creó este reporte
    id_tutor: int = Field(foreign_key="tutor.id_tutor", index=True)

    # --- Nuevos Campos del Reporte ---
    nombre_tutor: str = Field(max_length=300) # Guardamos el nombre completo para referencia
    periodo: str = Field(max_length=100, index=True)
    nombre_proyecto: str = Field(max_length=500)
    
    # Guardamos como un número entre 0 y 100
    porcentaje_avance: float = Field(default=0.0, sa_column=Column(Float))
    
    objetivo: str = Field(sa_column=Column(Text))
    descripcion: str = Field(sa_column=Column(Text))
    metas: str = Field(sa_column=Column(Text))
    actividades: str = Field(sa_column=Column(Text))
    
    # Guardamos los nombres de los archivos separados por comas, o como JSON
    documentos_anexados: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    conclusiones: str = Field(sa_column=Column(Text))
    observaciones: str = Field(sa_column=Column(Text))

    # --- Timestamps (Consistentes) ---
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
    # tutor: Optional["Tutor"] = Relationship(back_populates="reportes_g1")
    # Nota: Si activas esto, debes añadir 'reportes_g1: List["Reporte1"] = Relationship(back_populates="tutor")' al modelo Tutor.