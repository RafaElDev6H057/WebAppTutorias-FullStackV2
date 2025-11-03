# app/schemas/configuracion.py
from pydantic import BaseModel, Field
from typing import Literal

class ConfiguracionRead(BaseModel):
    reporte_integral_etapa: int

class ConfiguracionUpdate(BaseModel):
    # Usamos Literal para forzar que solo se puedan enviar estos valores
    reporte_integral_etapa: Literal[1, 2, 3]