# models/administrador.py

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

class Administrador(SQLModel, table=True):
    id_admin: Optional[int] = Field(default=None, primary_key=True)
    
    # ✅ 1. Añadimos index=True para optimizar el login
    usuario: str = Field(max_length=100, unique=True, index=True)
    contraseña: str

    # ✅ 2. Timestamps consistentes con el resto de la aplicación
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