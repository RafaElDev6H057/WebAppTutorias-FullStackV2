"""
Endpoints de la API para gestión de Tutorías.

Proporciona endpoints para operaciones CRUD con control de acceso dual
(administradores y tutores), consultas filtradas y carga masiva desde CSV.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query
from sqlmodel import Session, select, or_, func
from typing import List, Optional, Union

from app.database import get_session
from app.models.tutoria import Tutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate, TutoriaReadWithDetails, TutoriasPage
from app.services import tutoria_service
from app.models.alumno import Alumno
from app.models.tutor import Tutor
from app.core.dependencies import (
    get_current_admin_user,
    get_current_user,
    get_current_tutor_user,
    oauth2_scheme_admin,
    oauth2_scheme_tutor
)
from app.models.administrador import Administrador

router = APIRouter(prefix="/tutorias", tags=["Tutorias"])


def get_tutoria_or_404(id_tutoria: int, session: Session = Depends(get_session)) -> Tutoria:
    """
    Dependencia reutilizable que obtiene una tutoría por ID o lanza error 404.
    
    Args:
        id_tutoria: Identificador de la tutoría.
        session: Sesión de base de datos.
    
    Returns:
        Instancia de la tutoría encontrada.
    
    Raises:
        HTTPException: Si la tutoría no existe.
    """
    tutoria = session.get(Tutoria, id_tutoria)
    
    if not tutoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tutoría no existe."
        )
    
    return tutoria


@router.get(
    "/",
    response_model=List[TutoriaReadWithDetails],
    summary="Obtener todas las Tutorías (Solo Admin)"
)
def get_all_tutorias(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Obtiene una lista completa de todos los registros de tutoría.
    
    Solo accesible por administradores. No incluye paginación.
    
    Returns:
        Lista de todas las tutorías con detalles de alumno y tutor.
    """
    return session.exec(select(Tutoria)).all()


@router.get(
    "/{id_tutoria}",
    response_model=TutoriaReadWithDetails,
    summary="Obtener Tutoría por ID (Admin o Tutor)",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def get_tutoria_by_id(
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene los detalles de una tutoría específica.
    
    Accesible por administradores o por el tutor propietario de la tutoría.
    
    Raises:
        HTTPException: Si el tutor intenta acceder a una tutoría que no le pertenece.
    """
    if isinstance(current_user, Tutor) and tutoria.tutor_id != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta tutoría."
        )
    
    return tutoria


@router.post(
    "/",
    response_model=TutoriaReadWithDetails,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Tutoría Manualmente (Admin o Tutor)",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def create_tutoria(
    data: TutoriaCreate,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Crea un nuevo registro de tutoría manualmente.
    
    Los tutores solo pueden asignarse tutorías a sí mismos.
    Los administradores pueden asignar tutorías a cualquier tutor.
    
    Raises:
        HTTPException: Si un tutor intenta asignar la tutoría a otro tutor.
    """
    if isinstance(current_user, Tutor) and data.tutor_id != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para asignar esta tutoría a otro tutor."
        )
    
    return tutoria_service.create_tutoria(db=session, data=data)


@router.put(
    "/{id_tutoria}",
    response_model=TutoriaReadWithDetails,
    summary="Actualizar Tutoría (Admin o Tutor)",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def update_tutoria(
    data: TutoriaUpdate,
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Actualiza una tutoría existente.
    
    Accesible por administradores o por el tutor propietario de la tutoría.
    
    Raises:
        HTTPException: Si el tutor intenta modificar una tutoría que no le pertenece.
    """
    if isinstance(current_user, Tutor) and tutoria.tutor_id != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta tutoría."
        )
    
    return tutoria_service.update_tutoria(db=session, tutoria=tutoria, data=data)


@router.delete(
    "/{id_tutoria}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Tutoría (Admin o Tutor)",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def delete_tutoria(
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Elimina un registro de tutoría.
    
    Accesible por administradores o por el tutor propietario de la tutoría.
    Esta acción es permanente y no puede deshacerse.
    
    Raises:
        HTTPException: Si el tutor intenta eliminar una tutoría que no le pertenece.
    """
    if isinstance(current_user, Tutor) and tutoria.tutor_id != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta tutoría."
        )
    
    session.delete(tutoria)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/alumno/{id_alumno}",
    response_model=List[TutoriaReadWithDetails],
    summary="Obtener Tutorías por Alumno"
)
def get_tutorias_by_alumno(
    id_alumno: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene el historial completo de tutorías de un alumno específico.
    
    Returns:
        Lista de todas las tutorías del alumno con detalles de tutor.
    """
    tutorias = session.exec(
        select(Tutoria).where(Tutoria.alumno_id == id_alumno)
    ).all()
    
    return tutorias


@router.get(
    "/tutor/{id_tutor}",
    response_model=TutoriasPage,
    summary="Obtener Tutorías por Tutor",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def get_tutorias_by_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user),
    page: int = Query(1, gt=0, description="Número de página"),
    size: int = Query(10, gt=0, le=100, description="Tamaño de página"),
    search: Optional[str] = Query(None, min_length=3, description="Búsqueda por nombre o número de control")
):
    """
    Obtiene las tutorías asignadas a un tutor específico con paginación y búsqueda.
    
    Los tutores solo pueden consultar sus propias tutorías.
    Los administradores pueden consultar las tutorías de cualquier tutor.
    
    Args:
        id_tutor: ID del tutor a consultar.
        page: Número de página (inicia en 1).
        size: Cantidad de registros por página (máximo 100).
        search: Término de búsqueda por nombre, apellido o número de control del alumno.
    
    Returns:
        Página de tutorías con total de registros.
    
    Raises:
        HTTPException: Si el tutor intenta consultar tutorías de otro tutor.
    """
    is_allowed = False
    
    if isinstance(current_user, Administrador):
        is_allowed = True
    elif isinstance(current_user, Tutor) and current_user.id_tutor == id_tutor:
        is_allowed = True
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso."
        )
    
    base_query = select(Tutoria).join(Alumno).where(Tutoria.tutor_id == id_tutor)
    count_base_query = select(func.count(Tutoria.id_tutoria)).where(Tutoria.tutor_id == id_tutor) # type: ignore

    if search:
        search_term = f"%{search}%"
        search_filter = or_(
            Alumno.nombre.ilike(search_term), #type:ignore
            Alumno.apellido_p.ilike(search_term), #type:ignore
            Alumno.apellido_m.ilike(search_term), #type:ignore
            Alumno.num_control.ilike(search_term) #type:ignore
        )
        
        base_query = base_query.where(search_filter)
        count_base_query = count_base_query.join(Alumno).where(search_filter)
    
    total_tutorias = session.exec(count_base_query).one()
    offset = (page - 1) * size
    tutorias = session.exec(base_query.offset(offset).limit(size)).all()
    
    return TutoriasPage(total_tutorias=total_tutorias, tutorias=tutorias) #type:ignore


@router.post(
    "/upload-assignment",
    summary="Cargar Asignaciones desde CSV (Admin)",
    status_code=status.HTTP_200_OK
)
def upload_tutoria_assignment(
    file: UploadFile = File(..., description="Archivo CSV con formato específico de asignación"),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Procesa un archivo CSV para crear asignaciones masivas de tutorías.
    
    Solo accesible por administradores. El archivo debe contener metadata
    del periodo y tutor, seguido de la lista de números de control de alumnos.
    
    Returns:
        Resumen del procesamiento con tutorías creadas, errores y advertencias.
    
    Raises:
        HTTPException: Si el archivo no es CSV o hay errores de formato.
    """
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Se requiere un archivo CSV.")
    
    result = tutoria_service.process_assignment_csv(db=session, file=file)
    
    return result
