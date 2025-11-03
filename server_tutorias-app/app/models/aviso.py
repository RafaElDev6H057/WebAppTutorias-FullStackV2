# app/models/aviso.py

from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime, Text

class Aviso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    titulo: str = Field(index=True, max_length=255)
    
    # Usamos Text para permitir descripciones largas
    descripcion: str = Field(sa_column=Column(Text))
    
    link: Optional[str] = Field(default=None, max_length=1024)
    
    # Bandera para que el admin pueda publicar o despublicar (borrador)
    is_activo: bool = Field(default=False, nullable=False)

    # Timestamps para ordenar
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