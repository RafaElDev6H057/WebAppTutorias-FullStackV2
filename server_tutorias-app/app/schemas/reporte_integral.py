# app/schemas/reporte_integral.py

from pydantic import BaseModel, Field
from typing import Optional

# --- Esquema Base ---
# Contiene todos los campos del formulario del reporte
class ReporteIntegralBase(BaseModel):
    tutoria_grupal: int = Field(ge=0, default=0)
    tutoria_individual: int = Field(ge=0, default=0)
    seguimiento_1: Optional[str] = None
    seguimiento_2: Optional[str] = None
    seguimiento_3: Optional[str] = None
    jefatura_academica: int = Field(ge=0, default=0)
    ciencias_basicas: int = Field(ge=0, default=0)
    psicologia: int = Field(ge=0, default=0)
    materias_aprobadas: int = Field(ge=0, default=0)
    materias_no_aprobadas: Optional[str] = None

# --- Esquema para Crear ---
# Hereda del Base y añade el ID de la tutoría asociada
class ReporteIntegralCreate(ReporteIntegralBase):
    id_tutoria: int # Obligatorio al crear o actualizar vía POST

# --- Esquema para Leer ---
# Hereda del Base y añade los IDs generados por la BD
class ReporteIntegralRead(ReporteIntegralBase):
    id: int # ID del propio reporte
    id_tutoria: int # ID de la tutoría asociada

    class Config:
        from_attributes = True # Permite crear desde el modelo ORM

# --- Esquema para Actualizar (vía PUT) ---
# Todos los campos son opcionales para permitir actualizaciones parciales
class ReporteIntegralUpdate(BaseModel):
    tutoria_grupal: Optional[int] = Field(default=None, ge=0)
    tutoria_individual: Optional[int] = Field(default=None, ge=0)
    seguimiento_1: Optional[str] = None
    seguimiento_2: Optional[str] = None
    seguimiento_3: Optional[str] = None
    jefatura_academica: Optional[int] = Field(default=None, ge=0)
    ciencias_basicas: Optional[int] = Field(default=None, ge=0)
    psicologia: Optional[int] = Field(default=None, ge=0)
    materias_aprobadas: Optional[int] = Field(default=None, ge=0)
    materias_no_aprobadas: Optional[str] = None
    # Nota: No incluimos 'id_tutoria', ya que la relación no debería cambiarse al actualizar