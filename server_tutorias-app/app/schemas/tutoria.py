# app/schemas/tutoria.py

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.tutoria import EstadoTutoria

# Imports de esquemas básicos (sin cambios)
from app.schemas.alumno import AlumnoReadBasic
from app.schemas.tutor import TutorReadBasic


class TutoriaBase(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = EstadoTutoria.PENDIENTE
    observaciones: Optional[str] = None
    semestre: int = Field(..., ge=1, le=14)

class TutoriaCreate(TutoriaBase):
    alumno_id: int
    tutor_id: Optional[int] = None

class TutoriaUpdate(BaseModel):
    periodo: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[EstadoTutoria] = None
    observaciones: Optional[str] = None
    semestre: Optional[int] = Field(default=None, ge=1, le=14)
    tutor_id: Optional[int] = None

class TutoriaRead(TutoriaBase):
    id_tutoria: int
    alumno_id: int
    tutor_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    # ✅ --- NUEVO CAMPO AÑADIDO ---
    reporte_integral_guardado: bool
    # -----------------------------

    class Config:
        from_attributes = True

class TutoriaReadWithDetails(TutoriaRead):
    alumno: Optional[AlumnoReadBasic] = None
    tutor: Optional[TutorReadBasic] = None
    # 'reporte_integral_guardado' se hereda automáticamente de TutoriaRead

    class Config:
        from_attributes = True

class TutoriasPage(BaseModel):
    total_tutorias: int
    tutorias: List[TutoriaReadWithDetails]