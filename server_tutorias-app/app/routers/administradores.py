"""
Endpoints de la API para gestión de Administradores.

Proporciona endpoints para autenticación y operaciones CRUD de administradores.
Todos los endpoints (excepto login) requieren autenticación de administrador
con rol SUPER_ADMIN.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List
from datetime import timedelta

from app.database import get_session
from app.models.administrador import Administrador
from app.schemas.administrador import (
    AdministradorCreate,
    AdministradorRead,
    AdministradorUpdate,
    Token
)
from app.services import admin_service
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_current_admin_user

router = APIRouter(prefix="/administradores", tags=["Administradores"])


@router.post("/login", response_model=Token, summary="Login para Administradores")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """
    Autentica a un administrador y genera un token JWT.
    
    Cualquier rol de administrador (Super Admin, Psicología, etc.) puede
    hacer login por aquí.
    """
    admin = admin_service.authenticate_admin(db, form_data.username, form_data.password)
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # IMPORTANTE: Ahora el token podría incluir el rol si lo deseamos en el futuro,
    # pero por ahora con el 'sub' (usuario) es suficiente ya que el backend
    # busca al usuario en la BD en cada petición.
    access_token = security.create_access_token(
        data={"sub": admin.usuario},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/", 
    response_model=List[AdministradorRead], 
    summary="Obtener todos los Administradores",
    description="Devuelve la lista de administradores.\n\n**Requiere Rol:** SUPER_ADMIN.",
    responses={403: {"description": "Permisos insuficientes (Requiere Super Admin)"}}
)
def get_all_admins(
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Obtiene una lista completa de todos los administradores registrados.
    Solo accesible por SUPER_ADMIN.
    """
    return session.exec(select(Administrador)).all()


@router.get(
    "/{id_admin}", 
    response_model=AdministradorRead, 
    summary="Obtener Administrador por ID",
    description="Busca un administrador específico.\n\n**Requiere Rol:** SUPER_ADMIN.",
    responses={
        403: {"description": "Permisos insuficientes (Requiere Super Admin)"},
        404: {"description": "Administrador no encontrado"}
    }
)
def get_admin_by_id(
    id_admin: int,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Obtiene los datos de un administrador específico por su ID.
    Solo accesible por SUPER_ADMIN.
    """
    admin = session.get(Administrador, id_admin)
    
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    return admin


@router.post(
    "/",
    response_model=AdministradorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Administrador",
    description="Crea un nuevo administrador (o usuario de departamento).\n\n**Requiere Rol:** SUPER_ADMIN.",
    responses={
        403: {"description": "Permisos insuficientes (Requiere Super Admin)"},
        409: {"description": "El nombre de usuario ya existe"}
    }
)
def create_admin(
    data: AdministradorCreate,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Crea un nuevo administrador en el sistema.
    
    Gracias a que actualizamos el schema AdministradorCreate, aquí
    puedes enviar el campo "rol" para crear usuarios de Psicología, etc.
    """
    return admin_service.create_admin(db=session, data=data)


@router.put(
    "/{id_admin}", 
    response_model=AdministradorRead, 
    summary="Actualizar un Administrador",
    description="Actualiza datos (usuario, contraseña, rol).\n\n**Requiere Rol:** SUPER_ADMIN.",
    responses={
        403: {"description": "Permisos insuficientes (Requiere Super Admin)"},
        404: {"description": "Administrador no encontrado"}
    }
)
def update_admin(
    id_admin: int,
    data: AdministradorUpdate,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Actualiza los datos de un administrador existente.
    Solo accesible por SUPER_ADMIN.
    """
    admin_to_update = session.get(Administrador, id_admin)
    
    if not admin_to_update:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    return admin_service.update_admin(db=session, admin=admin_to_update, data=data)


@router.delete(
    "/{id_admin}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Eliminar un Administrador",
    description="Elimina permanentemente un administrador.\n\n**Requiere Rol:** SUPER_ADMIN.",
    responses={
        403: {"description": "Permisos insuficientes (Requiere Super Admin)"},
        404: {"description": "Administrador no encontrado"}
    }
)
def delete_admin(
    id_admin: int,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Elimina un administrador del sistema.
    Solo accesible por SUPER_ADMIN.
    """
    admin_to_delete = session.get(Administrador, id_admin)
    
    if not admin_to_delete:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    session.delete(admin_to_delete)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)