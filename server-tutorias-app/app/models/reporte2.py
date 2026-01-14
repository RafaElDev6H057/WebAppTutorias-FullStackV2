"""
Modelo de base de datos para la entidad Reporte2.

Define la estructura de la tabla para el SEGUNDO reporte (Final) de actividades
de tutoría grupal, enfocado en resultados obtenidos y conclusiones.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, Text, Float, Column
from typing import Optional
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class Reporte2(SQLModel, table=True):
    """
    Representa el REPORTE FINAL (Reporte 2) de un proyecto de tutoría grupal.
    
    Este reporte se genera al finalizar el periodo y contrasta los objetivos
    originales con los resultados reales obtenidos, documentando las
    actividades finales y conclusiones.
    
    Attributes:
        id: Identificador único del reporte.
        id_tutor: ID del tutor que creó el reporte.
        nombre_tutor: Nombre completo del tutor (snapshot histórico).
        periodo: Periodo académico.
        nombre_proyecto: Título del proyecto (debe coincidir o dar continuidad al Reporte 1).
        porcentaje_avance: Porcentaje final de progreso (usualmente 100% o cercano).
        objetivo: Objetivo general trabajado.
        descripcion: Descripción del desarrollo del proyecto.
        metas: Metas alcanzadas.
        actividades: Actividades realizadas (enfocadas en el cierre).
        documentos_anexados: Archivos adjuntos finales.
        conclusiones: Reflexión final y resultados.
        observaciones: Comentarios de cierre.
        created_at: Fecha de creación.
        updated_at: Fecha de última edición.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_tutor: int = Field(foreign_key="tutor.id_tutor", index=True)
    
    nombre_tutor: str = Field(max_length=300)
    periodo: str = Field(max_length=100, index=True)
    nombre_proyecto: str = Field(max_length=500)
    
    # En el Reporte 2, este valor es crucial para medir el éxito
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