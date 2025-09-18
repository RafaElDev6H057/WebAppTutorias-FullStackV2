# models/tutor.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone # Importar timezone
from sqlalchemy import Column, DateTime # Necesario para el onupdate

if TYPE_CHECKING:
    from app.models.tutoria import Tutoria


class Tutor(SQLModel, table=True):
    id_tutor: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido_p: str = Field(max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    especialidad: str = Field(max_length=100)
    correo: str = Field(index=True, unique=True, max_length=255) # max_length es buena práctica
    contraseña: str
    telefono: str = Field(max_length=20)

    # ✅ 1. Usamos timestamps con zona horaria para consistencia
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    # ✅ 2. Hacemos que updated_at se actualice automáticamente
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )

    tutorias: List["Tutoria"] = Relationship(back_populates="tutor")