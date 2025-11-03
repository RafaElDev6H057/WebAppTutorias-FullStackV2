# app/models/configuracion.py
from sqlmodel import SQLModel, Field
from typing import Optional

class ConfiguracionSistema(SQLModel, table=True):
    # Usamos un ID fijo (1) para que siempre sea la misma fila
    id: Optional[int] = Field(default=1, primary_key=True)
    
    # 1 = Solo Seguimiento 1
    # 2 = Seguimiento 1 y 2
    # 3 = Reporte Completo (todo habilitado)
    reporte_integral_etapa: int = Field(default=1, nullable=False)