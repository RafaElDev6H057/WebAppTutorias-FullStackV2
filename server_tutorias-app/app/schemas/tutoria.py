# app/schemas/tutoria.py

from typing import Optional, List # Asegúrate que List esté importado
from datetime import datetime # Quitamos 'time'
from pydantic import BaseModel, Field
from app.models.tutoria import EstadoTutoria # Quitamos DiaSemana

# Imports de esquemas básicos (sin cambios)
from app.schemas.alumno import AlumnoReadBasic
from app.schemas.tutor import TutorReadBasic


class TutoriaBase(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = EstadoTutoria.PENDIENTE
    observaciones: Optional[str] = None
    semestre: int = Field(..., ge=1, le=14)
    # ❗ Campos eliminados: es_activa, dia, hora

class TutoriaCreate(TutoriaBase):
    alumno_id: int
    tutor_id: Optional[int] = None
    # No necesita periodo aquí si se crea manualmente? O sí? Lo dejamos por si acaso.

class TutoriaUpdate(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = None
    observaciones: Optional[str] = None
    semestre: Optional[int] = Field(default=None, ge=1, le=14)
    tutor_id: Optional[int] = None
    # ❗ Campos eliminados: es_activa, dia, hora

class TutoriaRead(TutoriaBase):
    id_tutoria: int
    alumno_id: int
    tutor_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    # ❗ Campos heredados eliminados: es_activa, dia, hora

    class Config:
        from_attributes = True

class TutoriaReadWithDetails(TutoriaRead):
    alumno: Optional[AlumnoReadBasic] = None
    tutor: Optional[TutorReadBasic] = None
    # ❗ Campos heredados eliminados: es_activa, dia, hora

    class Config:
        from_attributes = True

class TutoriasPage(BaseModel):
    total_tutorias: int
    tutorias: List[TutoriaReadWithDetails]