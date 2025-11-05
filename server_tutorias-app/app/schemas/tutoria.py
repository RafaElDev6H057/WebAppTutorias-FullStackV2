"""
Esquemas Pydantic para validación y serialización de datos de Tutoría.

Define los diferentes esquemas utilizados en las operaciones CRUD de tutorías,
incluyendo esquemas con detalles anidados de alumno y tutor.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.tutoria import EstadoTutoria
from app.schemas.alumno import AlumnoReadBasic
from app.schemas.tutor import TutorReadBasic


class TutoriaBase(BaseModel):
    """
    Esquema base con los campos comunes de Tutoría.
    
    Incluye validaciones para periodo, estado, observaciones y semestre.
    """
    
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = EstadoTutoria.PENDIENTE
    observaciones: Optional[str] = None
    semestre: int = Field(..., ge=1, le=14)


class TutoriaCreate(TutoriaBase):
    """
    Esquema para la creación de una nueva tutoría.
    
    Requiere asignar un alumno y opcionalmente un tutor.
    """
    
    alumno_id: int
    tutor_id: Optional[int] = None


class TutoriaUpdate(BaseModel):
    """
    Esquema para la actualización parcial de una tutoría.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = None
    observaciones: Optional[str] = None
    semestre: Optional[int] = Field(default=None, ge=1, le=14)
    tutor_id: Optional[int] = None


class TutoriaRead(TutoriaBase):
    """
    Esquema para lectura de datos de tutoría.
    
    Incluye identificadores de relaciones y metadatos de timestamp.
    """
    
    id_tutoria: int
    alumno_id: int
    tutor_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    reporte_integral_guardado: bool
    
    model_config = ConfigDict(from_attributes=True)


class TutoriaReadWithDetails(TutoriaRead):
    """
    Esquema extendido de lectura con detalles anidados.
    
    Incluye información básica del alumno y tutor asociados a la tutoría.
    Hereda automáticamente todos los campos de TutoriaRead, incluyendo
    reporte_integral_guardado.
    """
    
    alumno: Optional[AlumnoReadBasic] = None
    tutor: Optional[TutorReadBasic] = None
    
    model_config = ConfigDict(from_attributes=True)


class TutoriasPage(BaseModel):
    """
    Esquema para respuesta paginada de tutorías.
    
    Incluye el total de registros y la lista de tutorías con detalles
    de la página actual.
    """
    
    total_tutorias: int
    tutorias: List[TutoriaReadWithDetails]
