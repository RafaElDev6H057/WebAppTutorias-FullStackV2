"""
Modelo de base de datos para la entidad Reporte1.

Define la estructura de la tabla de reportes de proyectos de tutores,
incluyendo información sobre objetivos, metas, actividades y progreso
de iniciativas grupales de tutoría.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, Text, Float, Column
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.tutor import Tutor


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Reporte1(SQLModel, table=True):
    """
    Representa un reporte de proyecto de tutoría grupal creado por un tutor.
    
    Este reporte documenta proyectos e iniciativas desarrolladas por el tutor
    durante un periodo académico, incluyendo objetivos, avances, actividades
    realizadas y documentación de soporte.
    
    Attributes:
        id: Identificador único del reporte.
        id_tutor: ID del tutor que creó el reporte (relación obligatoria).
        nombre_tutor: Nombre completo del tutor (guardado para referencia histórica).
        periodo: Periodo académico del reporte (ej. "Enero-Junio 2025").
        nombre_proyecto: Título del proyecto o iniciativa.
        porcentaje_avance: Porcentaje de progreso del proyecto (0-100).
        objetivo: Objetivo general del proyecto.
        descripcion: Descripción detallada del proyecto.
        metas: Metas específicas a alcanzar.
        actividades: Actividades realizadas durante el periodo.
        documentos_anexados: Nombres de archivos adjuntos (separados por comas o JSON).
        conclusiones: Conclusiones obtenidas del proyecto.
        observaciones: Observaciones adicionales del tutor.
        created_at: Fecha y hora de creación del reporte.
        updated_at: Fecha y hora de última actualización del reporte.
        tutor: Relación con el modelo Tutor.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_tutor: int = Field(foreign_key="tutor.id_tutor", index=True)
    
    nombre_tutor: str = Field(max_length=300)
    periodo: str = Field(max_length=100, index=True)
    nombre_proyecto: str = Field(max_length=500)
    porcentaje_avance: float = Field(default=0.0, sa_column=Column(Float))
    objetivo: str = Field(sa_column=Column(Text))
    descripcion: str = Field(sa_column=Column(Text))
    metas: str = Field(sa_column=Column(Text))
    actividades: str = Field(sa_column=Column(Text))
    documentos_anexados: Optional[str] = Field(default=None, sa_column=Column(Text))
    conclusiones: str = Field(sa_column=Column(Text))
    observaciones: str = Field(sa_column=Column(Text))
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
    
    # tutor: Optional["Tutor"] = Relationship(back_populates="reportes_g1")
