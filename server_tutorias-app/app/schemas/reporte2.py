from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reporte2Base(BaseModel):
    nombre_tutor: str
    carrera: str
    semestre: str
    grupo: str
    periodo: str
    fecha_corte: datetime
    total_alumnos: int
    baja_definitiva: bool
    cantidad_baja: Optional[int] = None
    alumnos_baja: Optional[str] = None
    canalizacion_psicologia: bool
    retroalimentacion_psicologia: Optional[bool] = None
    atiende_discapacidad: bool
    alumnos_discapacidad: Optional[str] = None
    alumnos_asesoria: Optional[str] = None
    porcentaje_avance: Optional[float] = None
    actividades_realizadas: Optional[str] = None

class Reporte2Create(Reporte2Base):
    pass

class Reporte2Read(Reporte2Base):
    id_reporte: int

    class Config:
        from_attributes = True

class Reporte2Update(BaseModel):
    nombre_tutor: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[str] = None
    grupo: Optional[str] = None
    periodo: Optional[str] = None
    fecha_corte: Optional[datetime] = None
    total_alumnos: Optional[int] = None
    baja_definitiva: Optional[bool] = None
    cantidad_baja: Optional[int] = None
    alumnos_baja: Optional[str] = None
    canalizacion_psicologia: Optional[bool] = None
    retroalimentacion_psicologia: Optional[bool] = None
    atiende_discapacidad: Optional[bool] = None
    alumnos_discapacidad: Optional[str] = None
    alumnos_asesoria: Optional[str] = None
    porcentaje_avance: Optional[float] = None
    actividades_realizadas: Optional[str] = None