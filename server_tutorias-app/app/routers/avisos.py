# app/routers/aviso.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List

# Imports de la app
from app.database import get_session
from app.models.aviso import Aviso
from app.schemas.aviso import AvisoCreate, AvisoRead, AvisoUpdate
from app.services import aviso_service

# Imports para seguridad
from app.core.dependencies import get_current_admin_user, get_current_alumno_user
from app.models.administrador import Administrador
from app.models.alumno import Alumno

# --- Configuración del Router ---
router = APIRouter(prefix="/avisos", tags=["Avisos"])


# ==================================
# === ENDPOINT PARA ALUMNOS ===
# ==================================

@router.get(
    "/", 
    response_model=List[AvisoRead], 
    summary="Obtener avisos públicos (para Alumnos)"
)
def get_publicos_avisos(
    session: Session = Depends(get_session),
    # Protegido: Solo un alumno autenticado puede ver los avisos
    current_alumno: Alumno = Depends(get_current_alumno_user) 
):
    """
    Obtiene una lista de todos los avisos ACTIVOS (is_activo = True)
    ordenados del más reciente al más antiguo.
    """
    return aviso_service.get_avisos_publicos(db=session)


# =======================================
# === ENDPOINTS DE GESTIÓN (ADMINS) ===
# =======================================

@router.get(
    "/admin/todos", 
    response_model=List[AvisoRead], 
    summary="Obtener TODOS los avisos (Admin)"
)
def get_todos_los_avisos(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """
    Obtiene TODOS los avisos (activos e inactivos) para el panel
    de administración, ordenados del más reciente al más antiguo.
    """
    return aviso_service.get_avisos_todos(db=session)

@router.post(
    "/admin", 
    response_model=AvisoRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo aviso (Admin)"
)
def create_aviso(
    data: AvisoCreate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """
    Crea un nuevo aviso. Por defecto, 'is_activo' será False (borrador)
    a menos que se especifique lo contrario en el JSON.
    """
    return aviso_service.create_aviso(db=session, data=data)

@router.put(
    "/admin/{aviso_id}", 
    response_model=AvisoRead, 
    summary="Actualizar un aviso (Admin)"
)
def update_aviso(
    aviso_id: int,
    data: AvisoUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """
    Actualiza cualquier campo de un aviso existente, incluyendo
    publicarlo (is_activo = True) o despublicarlo (is_activo = False).
    """
    return aviso_service.update_aviso(db=session, aviso_id=aviso_id, data=data)

@router.delete(
    "/admin/{aviso_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un aviso (Admin)"
)
def delete_aviso(
    aviso_id: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """
    Elimina permanentemente un aviso de la base de datos.
    """
    aviso_service.delete_aviso(db=session, aviso_id=aviso_id)
    # Devuelve 204 No Content automáticamente si no hay cuerpo
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- FIN DEL ARCHIVO ---