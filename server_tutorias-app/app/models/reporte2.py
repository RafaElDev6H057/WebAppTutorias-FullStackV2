from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

class Reporte2(SQLModel, table=True):
    id_reporte: Optional[int] = Field(default=None, primary_key=True)

    nombre_tutor: str = Field()
    carrera: str = Field()
    semestre: str = Field()
    grupo: str = Field()
    periodo: str = Field()
    fecha_corte: datetime = Field()

    total_alumnos: int = Field()
    baja_definitiva: bool = Field()
    cantidad_baja: Optional[int] = Field(default=None)
    alumnos_baja: Optional[str] = Field(default=None)

    canalizacion_psicologia: bool = Field()
    retroalimentacion_psicologia: Optional[bool] = Field(default=None)
    atiende_discapacidad: bool = Field()
    alumnos_discapacidad: Optional[str] = Field(default=None)

    alumnos_asesoria: Optional[str] = Field(default=None)

    porcentaje_avance: Optional[float] = Field(default=None)
    actividades_realizadas: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        ),
    )