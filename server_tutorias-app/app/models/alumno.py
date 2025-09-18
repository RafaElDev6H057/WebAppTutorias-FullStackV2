# models/alumno.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import enum
from sqlalchemy import Column, DateTime # 👈 Importar Column y DateTime

# Import relativo para evitar problemas de importación circular
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .tutoria import Tutoria

# Definimos un Enum para el estado del alumno
class EstadoAlumno(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    EGRESADO = "egresado"
    BAJA = "baja"


class Alumno(SQLModel, table=True):

    id_alumno: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido_p: str = Field(max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    
    num_control: str = Field(max_length=50, unique=True, index=True) 
    contraseña: str
    carrera: str = Field(max_length=100)
    
    semestre_actual: int = Field(ge=1, le=14)
    estado: str = Field(default=EstadoAlumno.ACTIVO, max_length=50)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    # ✅ Se añade el campo 'updated_at' para consistencia
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )
    
    tutorias: List["Tutoria"] = Relationship(back_populates="alumno")