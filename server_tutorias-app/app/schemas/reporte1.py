from pydantic import BaseModel
from typing import Optional

class Reporte1Base(BaseModel):
    nombre_tutor: str
    carrera: str
    semestre: str
    grupo: str
    periodo: str
    total_alumnos: int
    hay_desercion: bool
    cantidad_desercion: Optional[int] = None
    alumnos_desercion: Optional[str] = None
    canalizacion_psicologia: bool
    atiende_discapacidad: bool
    alumnos_discapacidad: Optional[str] = None
    alumnos_reprobados: bool
    alumnos_materias_reprobadas: Optional[str] = None
    alumnos_asesoria: Optional[str] = None
    porcentaje_proyecto: float
    objetivo_proyecto: Optional[str] = None
    descripcion_proyecto: Optional[str] = None
    metas_proyecto: Optional[str] = None
    actividades_realizadas: Optional[str] = None
    conclusion: Optional[str] = None
    observaciones: Optional[str] = None

class Reporte1Create(Reporte1Base):
    pass

class Reporte1Read(Reporte1Base):
    id_reporte: int

    class Config:
        from_attributes = True

class Reporte1Update(BaseModel):
    nombre_tutor: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[str] = None
    grupo: Optional[str] = None
    periodo: Optional[str] = None
    total_alumnos: Optional[int] = None
    hay_desercion: Optional[bool] = None
    cantidad_desercion: Optional[int] = None
    alumnos_desercion: Optional[str] = None
    canalizacion_psicologia: Optional[bool] = None
    atiende_discapacidad: Optional[bool] = None
    alumnos_discapacidad: Optional[str] = None
    alumnos_reprobados: Optional[bool] = None
    alumnos_materias_reprobadas: Optional[str] = None
    alumnos_asesoria: Optional[str] = None
    porcentaje_proyecto: Optional[float] = None
    objetivo_proyecto: Optional[str] = None
    descripcion_proyecto: Optional[str] = None
    metas_proyecto: Optional[str] = None
    actividades_realizadas: Optional[str] = None
    conclusion: Optional[str] = None
    observaciones: Optional[str] = None