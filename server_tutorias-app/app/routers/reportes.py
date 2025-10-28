# app/routers/reportes.py

from fastapi import APIRouter, Depends, Response, status, HTTPException # Añadido HTTPException
from sqlmodel import Session
from typing import List, Union # Añadido List y Union

# Imports de la app
from app.database import get_session
from app.models.reporte_integral import ReporteIntegral # Importar el modelo
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralRead, ReporteIntegralUpdate # Importar esquemas
from app.services import reporte_integral_service
# Imports para otros reportes (sin cambios)
from app.schemas.reporte1 import Reporte1Create, Reporte1Read
from app.services import reporte1_service
from app.schemas.reporte2 import Reporte2Create, Reporte2Read
from app.services import reporte2_service
# Imports para seguridad
from app.core.dependencies import get_current_user # Usamos la dependencia combinada
from app.models.administrador import Administrador
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria # Necesario para verificar permisos

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# ==================================
# === Reporte Integral (CRUD) ===
# ==================================

# --- POST /integral (Crear o Actualizar) ---
@router.post(
    "/integral",
    response_model=ReporteIntegralRead,
    status_code=status.HTTP_201_CREATED, # Mantenemos 201 aunque actualice, común en Upsert POST
    summary="Crear o Actualizar Reporte Integral"
)
def handle_create_or_update_reporte(
    data: ReporteIntegralCreate,
    session: Session = Depends(get_session),
    # Protección: Solo Admins o Tutores pueden crear/actualizar
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Crea un nuevo reporte integral si no existe para la tutoría,
    o actualiza el existente. Requiere autenticación (Admin o Tutor).
    Actualiza la bandera 'reporte_integral_guardado' en la Tutoria.
    """
    # --- Validación de Permisos Adicional (Tutor solo puede afectar sus tutorías) ---
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, data.id_tutoria)
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para crear/modificar un reporte para esta tutoría."
            )
    # --- Fin Validación ---

    reporte = reporte_integral_service.create_or_update_reporte(db=session, data=data)
    return reporte

# --- GET /integral/tutoria/{id_tutoria} (Leer por ID de Tutoría) ---
@router.get(
    "/integral/tutoria/{id_tutoria}",
    response_model=ReporteIntegralRead,
    summary="Obtener Reporte Integral por ID de Tutoría"
)
def handle_get_reporte_by_tutoria(
    id_tutoria: int,
    session: Session = Depends(get_session),
    # Protección: Solo Admins o el Tutor asociado a esa tutoría
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene el reporte integral asociado a una tutoría específica.
    Requiere autenticación (Admin o el Tutor de la tutoría).
    Devuelve 404 si el reporte no existe aún.
    """
    reporte = reporte_integral_service.get_reporte_by_tutoria(db=session, id_tutoria=id_tutoria)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte Integral no encontrado para esta tutoría.")

    # --- Validación de Permisos ---
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, id_tutoria) # Volvemos a buscar la tutoría para verificar
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este reporte."
            )
    # --- Fin Validación ---

    return reporte

# --- GET /integral/{reporte_id} (Leer por ID de Reporte) ---
@router.get(
    "/integral/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Obtener Reporte Integral por ID"
)
def handle_get_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene un reporte integral específico por su ID.
    Requiere autenticación (Admin o el Tutor asociado).
    """
    reporte = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    # get_reporte ya lanza 404 si no existe, pero añadimos el check para el linter y claridad
    if not reporte:
        # Esta línea teóricamente no se alcanzará debido al 404 en el servicio,
        # pero satisface al linter.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado.")

    # --- Validación de Permisos ---
    if isinstance(current_user, Tutor):
        # Ahora que sabemos que 'reporte' no es None, podemos acceder a 'id_tutoria'
        tutoria_asociada = session.get(Tutoria, reporte.id_tutoria)
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso.")
    # --- Fin Validación ---

    return reporte

# --- PUT /integral/{reporte_id} (Actualizar) ---
@router.put(
    "/integral/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Actualizar Reporte Integral"
)
def handle_update_reporte(
    reporte_id: int,
    data: ReporteIntegralUpdate,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Actualiza un reporte integral existente.
    Requiere autenticación (Admin o el Tutor asociado).
    """
    reporte_existente = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    if not reporte_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado.") # Redundante pero claro

    # --- Validación de Permisos ---
    if isinstance(current_user, Tutor):
        # Ahora 'reporte_existente' no es None
        tutoria_asociada = session.get(Tutoria, reporte_existente.id_tutoria)
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso.")
    # --- Fin Validación ---

    reporte_actualizado = reporte_integral_service.update_reporte(
        db=session, reporte_id=reporte_id, data=data
    )
    return reporte_actualizado

# --- DELETE /integral/{reporte_id} (Eliminar) ---
@router.delete(
    "/integral/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Reporte Integral"
)
def handle_delete_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Elimina un reporte integral existente.
    Requiere autenticación (Admin o el Tutor asociado).
    """
    reporte_existente = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    if not reporte_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado.") # Redundante pero claro

    # --- Validación de Permisos ---
    if isinstance(current_user, Tutor):
        # Ahora 'reporte_existente' no es None
        tutoria_asociada = session.get(Tutoria, reporte_existente.id_tutoria)
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso.")
    # --- Fin Validación ---

    reporte_integral_service.delete_reporte(db=session, reporte_id=reporte_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================
# === Otros Reportes (Generales) ===
# ==================================
# Estos endpoints probablemente solo deberían ser accesibles por Admins o Tutores específicos
# Añadir protección similar si es necesario.

@router.post( "/general-1", response_model=Reporte1Read, status_code=status.HTTP_201_CREATED)
def handle_create_reporte1(
    data: Reporte1Create,
    session: Session = Depends(get_session),
    # Ejemplo: current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte1 = reporte1_service.create_reporte1(db=session, data=data)
    return reporte1

@router.post("/general-2", response_model=Reporte2Read, status_code=status.HTTP_201_CREATED)
def handle_create_reporte2(
    data: Reporte2Create,
    session: Session = Depends(get_session),
    # Ejemplo: current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte2 = reporte2_service.create_reporte2(db=session, data=data)
    return reporte2

# --- FIN DEL ARCHIVO ---