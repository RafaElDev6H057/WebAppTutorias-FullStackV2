"""
Endpoints de la API para gestión de Avisos.

Proporciona endpoints para que los alumnos consulten avisos publicados
y para que los administradores gestionen la creación, edición y publicación
de avisos del sistema.
"""

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.aviso import AvisoCreate, AvisoRead, AvisoUpdate
from app.services import aviso_service
from app.core.dependencies import get_current_admin_user, get_current_alumno_user
from app.models.administrador import Administrador
from app.models.alumno import Alumno

router = APIRouter(prefix="/avisos", tags=["Avisos"])


@router.get(
    "/",
    response_model=List[AvisoRead],
    summary="Obtener avisos públicos (para Alumnos)"
)
def get_publicos_avisos(
    session: Session = Depends(get_session),
    current_alumno: Alumno = Depends(get_current_alumno_user)
):
    """
    Obtiene todos los avisos activos publicados.
    
    Solo accesible por alumnos autenticados. Retorna únicamente
    los avisos que han sido marcados como activos (is_activo=True),
    ordenados del más reciente al más antiguo.
    
    Returns:
        Lista de avisos activos.
    """
    return aviso_service.get_avisos_publicos(db=session)


@router.get(
    "/admin/todos",
    response_model=List[AvisoRead],
    summary="Obtener TODOS los avisos (Admin)"
)
def get_todos_los_avisos(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Obtiene todos los avisos del sistema (activos e inactivos).
    
    Solo accesible por administradores. Útil para el panel de administración
    donde se pueden ver tanto avisos publicados como borradores,
    ordenados del más reciente al más antiguo.
    
    Returns:
        Lista de todos los avisos del sistema.
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
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Crea un nuevo aviso en el sistema.
    
    Solo accesible por administradores. Por defecto, los avisos nuevos
    se crean en estado inactivo (borrador) a menos que se especifique
    is_activo=True en el JSON.
    
    Returns:
        Datos del aviso creado.
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
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Actualiza un aviso existente.
    
    Solo accesible por administradores. Permite actualizar cualquier campo
    del aviso, incluyendo publicarlo (is_activo=True) o despublicarlo
    (is_activo=False).
    
    Raises:
        HTTPException: Si el aviso no existe.
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
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Elimina permanentemente un aviso del sistema.
    
    Solo accesible por administradores. Esta acción es permanente
    y no puede deshacerse.
    
    Raises:
        HTTPException: Si el aviso no existe.
    """
    aviso_service.delete_aviso(db=session, aviso_id=aviso_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
