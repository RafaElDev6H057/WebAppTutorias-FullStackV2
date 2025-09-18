# schemas/tutoria.py

from typing import Optional
from datetime import time, datetime
from pydantic import BaseModel, Field
from app.models.tutoria import EstadoTutoria, DiaSemana

# ✅ Importamos los nuevos esquemas básicos que creamos
from app.schemas.alumno import AlumnoReadBasic
from app.schemas.tutor import TutorReadBasic


class TutoriaBase(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = EstadoTutoria.PENDIENTE
    observaciones: Optional[str] = None
    semestre: int = Field(..., ge=1, le=14)
    es_activa: bool = False
    dia: Optional[DiaSemana] = None
    hora: Optional[time] = None

class TutoriaCreate(TutoriaBase):
    alumno_id: int
    tutor_id: Optional[int] = None


class TutoriaUpdate(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = None
    observaciones: Optional[str] = None
    semestre: Optional[int] = Field(default=None, ge=1, le=14)
    es_activa: Optional[bool] = None
    dia: Optional[DiaSemana] = None
    hora: Optional[time] = None
    tutor_id: Optional[int] = None


class TutoriaRead(TutoriaBase):
    id_tutoria: int
    alumno_id: int
    tutor_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ✨ ¡LA MEJORA! Un esquema que devuelve los detalles del alumno y tutor.
class TutoriaReadWithDetails(TutoriaRead):
    alumno: Optional[AlumnoReadBasic] = None
    tutor: Optional[TutorReadBasic] = None

    class Config:
        from_attributes = True