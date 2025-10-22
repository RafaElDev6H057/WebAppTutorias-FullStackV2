# app/models/tutor.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

if TYPE_CHECKING:
    from app.models.tutoria import Tutoria


class Tutor(SQLModel, table=True):
    id_tutor: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido_p: str = Field(max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: str = Field(index=True, unique=True, max_length=255)
    contraseña: str
    
    # ✅ Añadimos la bandera, igual que en Alumno
    requires_password_change: bool = Field(default=True)

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

    tutorias: List["Tutoria"] = Relationship(back_populates="tutor")