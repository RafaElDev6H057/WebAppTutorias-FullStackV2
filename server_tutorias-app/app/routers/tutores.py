"""
Endpoints de la API para gestión de Tutores.

Proporciona endpoints para autenticación, operaciones CRUD, gestión de contraseñas
y consulta de tutores con paginación y búsqueda.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select, or_, func
from typing import Optional
from datetime import timedelta

from app.database import get_session
from app.models.tutor import Tutor
from app.schemas.tutor import (
    TutorCreate,
    TutorUpdate,
    TutorRead,
    TutorSetPassword,
    TutorUpdatePassword,
    TutorLogin,
    TutoresPage
)
from app.schemas.administrador import Token
from app.services import tutor_service
from app.core import security
from app.core.dependencies import get_current_admin_user, get_current_tutor_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.administrador import Administrador

router = APIRouter(prefix="/tutores", tags=["Tutores"])


@router.post("/login", response_model=Token, summary="Login para Tutores")
def login_tutor(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Autentica a un tutor y genera un token JWT.
    
    Acepta tanto contraseñas temporales (sin hashear) como permanentes (hasheadas).
    El tutor debe usar su correo electrónico como username.
    """
    tutor = tutor_service.get_tutor_by_email(session, form_data.username)
    
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    is_password_correct = False
    
    if tutor.requires_password_change:
        is_password_correct = (form_data.password == tutor.contraseña)
    else:
        is_password_correct = security.verify_password(form_data.password, tutor.contraseña)
    
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(tutor.id_tutor), "role": "tutor"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "rol": "tutor"}


@router.get("/me", response_model=TutorRead, summary="Obtener datos del Tutor autenticado")
def read_current_tutor(current_tutor: Tutor = Depends(get_current_tutor_user)):
    """
    Obtiene el perfil completo del tutor autenticado.
    
    Requiere token de autenticación de tutor en la cabecera Authorization.
    
    Returns:
        Datos completos del perfil del tutor.
    """
    return current_tutor


@router.post("/set-password", summary="Establecer contraseña permanente para un Tutor")
def set_password(data: TutorSetPassword, session: Session = Depends(get_session)):
    """
    Permite a un tutor establecer su contraseña permanente.
    
    El tutor debe proporcionar su contraseña temporal para validar su identidad
    antes de establecer una nueva contraseña permanente. No requiere autenticación.
    """
    return tutor_service.set_permanent_password(db=session, data=data)


@router.put("/change-password", summary="Cambiar la contraseña de un Tutor autenticado")
def change_tutor_password(
    data: TutorUpdatePassword,
    current_tutor: Tutor = Depends(get_current_tutor_user),
    session: Session = Depends(get_session)
):
    """
    Permite a un tutor autenticado cambiar su contraseña permanente.
    
    Requiere proporcionar la contraseña actual para validación.
    Solo disponible para tutores que ya establecieron su contraseña permanente.
    """
    return tutor_service.change_password(db=session, tutor=current_tutor, data=data)


@router.get("/", response_model=TutoresPage, summary="Obtener todos los Tutores (Admin)")
def get_tutores(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user),
    page: int = Query(1, gt=0, description="Número de página a solicitar"),
    size: int = Query(10, gt=0, le=100, description="Tamaño de la página (máximo 100)"),
    search: Optional[str] = Query(None, min_length=3, description="Término de búsqueda por nombre, apellido o correo")
):
    """
    Obtiene una lista paginada de tutores con búsqueda opcional.
    
    Accesible solo para administradores. Permite buscar por nombre,
    apellidos o correo electrónico.
    
    Args:
        page: Número de página (inicia en 1).
        size: Cantidad de registros por página (máximo 100).
        search: Término de búsqueda opcional (mínimo 3 caracteres).
    
    Returns:
        Página de tutores con total de registros.
    """
    query = select(Tutor)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Tutor.nombre.ilike(search_term), #type:ignore
                Tutor.apellido_p.ilike(search_term), #type:ignore
                Tutor.apellido_m.ilike(search_term), #type:ignore
                Tutor.correo.ilike(search_term) #type:ignore
            )
        )
    
    count_query = select(func.count()).select_from(query.subquery())
    total_tutores = session.exec(count_query).one()
    
    offset = (page - 1) * size
    tutores = session.exec(query.offset(offset).limit(size)).all()
    
    return TutoresPage(total_tutores=total_tutores, tutores=tutores)  #type:ignore


@router.get("/{id_tutor}", response_model=TutorRead, summary="Obtener un Tutor por ID (Admin)")
def get_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Obtiene los datos de un tutor específico por su ID.
    
    Solo accesible por administradores.
    
    Raises:
        HTTPException: Si el tutor no existe.
    """
    tutor = session.get(Tutor, id_tutor)
    
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    return tutor


@router.post(
    "/",
    response_model=TutorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Tutor (Admin)"
)
def create_tutor(
    data: TutorCreate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Crea un nuevo tutor manualmente.
    
    El tutor es creado con contraseña permanente (no temporal).
    Solo accesible por administradores.
    
    Returns:
        Datos del tutor creado.
    """
    return tutor_service.create_tutor(db=session, data=data)


@router.put("/{id_tutor}", response_model=TutorRead, summary="Actualizar un Tutor (Admin)")
def update_tutor(
    id_tutor: int,
    data: TutorUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Actualiza los datos de un tutor existente.
    
    Solo accesible por administradores.
    
    Raises:
        HTTPException: Si el tutor no existe.
    """
    tutor = session.get(Tutor, id_tutor)
    
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    return tutor_service.update_tutor(db=session, tutor=tutor, data=data)


@router.delete("/{id_tutor}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Tutor (Admin)")
def delete_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Elimina un tutor del sistema.
    
    Solo accesible por administradores.
    Esta acción es permanente y no puede deshacerse.
    
    Raises:
        HTTPException: Si el tutor no existe.
    """
    tutor = session.get(Tutor, id_tutor)
    
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    session.delete(tutor)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
