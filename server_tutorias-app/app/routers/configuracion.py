"""
Endpoints de la API para gestión de Configuración del Sistema.

Proporciona endpoints para consultar y actualizar la configuración global
que controla las etapas habilitadas del reporte integral de tutorías.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Union

from app.database import get_session
from app.services import configuracion_service
from app.schemas.configuracion import ConfiguracionRead, ConfiguracionUpdate
from app.core.dependencies import get_current_admin_user, get_current_user
from app.models.administrador import Administrador
from app.models.tutor import Tutor

router = APIRouter(prefix="/configuracion", tags=["Configuración"])


@router.get("/", response_model=ConfiguracionRead, summary="Obtener etapa actual del reporte")
def get_reporte_config(
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene la configuración actual del sistema.
    
    Retorna la etapa habilitada del reporte integral de tutorías:
    - Etapa 1: Solo Seguimiento 1
    - Etapa 2: Seguimiento 1 y 2
    - Etapa 3: Reporte completo (todas las secciones)
    
    Accesible por administradores y tutores autenticados.
    
    Returns:
        Configuración actual con la etapa activa.
    """
    config = configuracion_service.get_configuracion(db=session)
    return config


@router.put("/", response_model=ConfiguracionRead, summary="Actualizar etapa del reporte (Solo Admin)")
def update_reporte_config(
    data: ConfiguracionUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Actualiza la etapa habilitada del reporte integral.
    
    Permite cambiar la etapa actual del proceso de llenado del reporte:
    - 1: Solo permite Seguimiento 1
    - 2: Permite Seguimiento 1 y 2
    - 3: Habilita el reporte completo
    
    Solo accesible por administradores.
    
    Returns:
        Configuración actualizada con la nueva etapa.
    """
    config = configuracion_service.update_configuracion(db=session, data=data)
    return config
