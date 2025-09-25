# app/schemas/reporte_integral.py

from pydantic import BaseModel, Field
from typing import Optional

class ReporteIntegralBase(BaseModel):
    tutoria_grupal: int = Field(ge=0)
    tutoria_individual: int = Field(ge=0)
    seguimiento_1: Optional[str] = None
    seguimiento_2: Optional[str] = None
    seguimiento_3: Optional[str] = None
    jefatura_academica: int = Field(ge=0)
    ciencias_basicas: int = Field(ge=0)
    psicologia: int = Field(ge=0)
    materias_aprobadas: int = Field(ge=0)
    materias_no_aprobadas: Optional[str] = None

class ReporteIntegralCreate(ReporteIntegralBase):
    # Ya no se necesita el id_alumno, el schema queda igual que el base
    pass

class ReporteIntegralRead(ReporteIntegralBase):
    id: int

    class Config:
        from_attributes = True

# El schema Update ya no es necesario para esta lógica simple