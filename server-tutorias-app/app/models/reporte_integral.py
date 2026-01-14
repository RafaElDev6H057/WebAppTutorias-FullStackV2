"""
Modelo de base de datos para la entidad Reporte Integral.

Define la estructura de la tabla de reportes integrales que almacenan
información detallada de seguimiento y evaluación de las tutorías, incluyendo
asistencias, canalizaciones y materias del alumno.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.tutoria import Tutoria


def get_utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class ReporteIntegral(SQLModel, table=True):
    """
    Representa un reporte integral de seguimiento de tutoría.
    
    Cada reporte está asociado a una tutoría específica y contiene
    información sobre asistencias, seguimientos narrativos, canalizaciones
    y desempeño académico del alumno.
    
    Attributes:
        id: Identificador único del reporte.
        id_tutoria: ID de la tutoría asociada (relación obligatoria).
        tutoria_grupal: Número de tutorías grupales realizadas.
        tutoria_individual: Número de tutorías individuales realizadas.
        seguimiento_1: Texto libre del primer seguimiento (máx 500 caracteres).
        seguimiento_2: Texto libre del segundo seguimiento (máx 500 caracteres).
        seguimiento_3: Texto libre del tercer seguimiento (máx 500 caracteres).
        jefatura_academica: Número de canalizaciones a jefatura académica.
        ciencias_basicas: Número de canalizaciones a ciencias básicas.
        psicologia: Número de canalizaciones a psicología.
        materias_aprobadas: Cantidad de materias aprobadas por el alumno.
        materias_no_aprobadas: Texto con lista/detalle de materias no aprobadas.
        created_at: Fecha y hora de creación del reporte.
        updated_at: Fecha y hora de última actualización del reporte.
        tutoria: Relación con el modelo Tutoria.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_tutoria: int = Field(foreign_key="tutoria.id_tutoria", index=True)
    
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
    
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now
    )
    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), #type: ignore
        default_factory=get_utc_now,
        sa_column_kwargs={"onupdate": get_utc_now}
    )
    
    # tutoria: Optional["Tutoria"] = Relationship(back_populates="reportes_integrales")
