# app/routers/configuracion.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.services import configuracion_service
from app.schemas.configuracion import ConfiguracionRead, ConfiguracionUpdate
from app.core.dependencies import get_current_admin_user, get_current_user
from app.models.administrador import Administrador
from typing import Union
from app.models.tutor import Tutor

router = APIRouter(prefix="/configuracion", tags=["Configuración"])

@router.get("/", response_model=ConfiguracionRead, summary="Obtener etapa actual del reporte")
def get_reporte_config(
    session: Session = Depends(get_session),
    # Protegido: Admin o Tutor pueden VER la config
    current_user: Union[Administrador, Tutor] = Depends(get_current_user) 
):
    """
    Obtiene la etapa actual habilitada para el Reporte Integral (1, 2 o 3).
    """
    config = configuracion_service.get_configuracion(db=session)
    return config

@router.put("/", response_model=ConfiguracionRead, summary="Actualizar etapa del reporte (Solo Admin)")
def update_reporte_config(
    data: ConfiguracionUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Solo Admin
):
    """
    Actualiza la etapa de llenado del Reporte Integral.
    (1=Seguimiento 1, 2=Seguimiento 2, 3=Reporte Completo)
    """
    config = configuracion_service.update_configuracion(db=session, data=data)
    return config