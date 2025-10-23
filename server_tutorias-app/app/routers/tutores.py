# app/routers/tutores.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm # Removed unused OAuth2PasswordBearer here
from sqlmodel import Session, select
from typing import List
from datetime import timedelta

# Imports
from app.database import get_session
from app.models.tutor import Tutor
from app.schemas.tutor import (
    TutorCreate, TutorUpdate, TutorRead,
    TutorSetPassword, TutorUpdatePassword, TutorLogin
)
from app.schemas.administrador import Token
from app.services import tutor_service
from app.core import security
from app.core.dependencies import get_current_admin_user, get_current_tutor_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.administrador import Administrador

# --- Router Setup ---
router = APIRouter(prefix="/tutores", tags=["Tutores"])

print("--- CARGANDO ROUTER DE TUTORES (VERSIÓN COMPLETA) ---")

# ============================================
# === ENDPOINTS PARA AUTENTICACIÓN DE TUTOR ===
# ============================================

@router.post("/login", response_model=Token, summary="Login para Tutores")
def login_tutor(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Endpoint de login exclusivo para Tutores.
    Implementa la lógica dual para contraseñas temporales y permanentes.
    """
    tutor = tutor_service.get_tutor_by_email(session, form_data.username) # El 'username' es el correo

    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- Lógica de Login Dual ---
    is_password_correct = False
    if tutor.requires_password_change:
        # Contraseña temporal (texto plano)
        is_password_correct = (form_data.password == tutor.contraseña)
    else:
        # Contraseña permanente (hasheada)
        is_password_correct = security.verify_password(form_data.password, tutor.contraseña)

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"DEBUG LOGIN (Rebuild): Creando token para tutor ID = {tutor.id_tutor}")

    # --- Creación del Token ---
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(tutor.id_tutor), "role": "tutor"},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/set-password", summary="Establecer contraseña permanente para un Tutor")
def set_password(data: TutorSetPassword, session: Session = Depends(get_session)):
    """
    Permite a un tutor con contraseña temporal establecer su
    contraseña final y segura. No requiere token.
    """
    print("DEBUG REBUILD ENDPOINT: POST /set-password called.")
    return tutor_service.set_permanent_password(db=session, data=data)

@router.put("/change-password", summary="Cambiar la contraseña de un Tutor autenticado")
def change_tutor_password(
    data: TutorUpdatePassword,
    current_tutor: Tutor = Depends(get_current_tutor_user), # Protegido por token de Tutor
    session: Session = Depends(get_session)
):
    """
    Permite a un tutor autenticado (con contraseña hasheada)
    cambiar su contraseña.
    """
    print(f"DEBUG REBUILD ENDPOINT: change_tutor_password called.")
    return tutor_service.change_password(db=session, tutor=current_tutor, data=data)


# ===========================================
# === ENDPOINTS DE GESTIÓN (SOLO ADMINS) ===
# ===========================================

@router.get("/", response_model=List[TutorRead], summary="Obtener todos los Tutores (Admin)")
def get_tutores(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido por token de Admin
):
    """Obtiene una lista de todos los tutores registrados."""
    print("DEBUG REBUILD ENDPOINT: GET / called.")
    return session.exec(select(Tutor)).all()

@router.get("/{id_tutor}", response_model=TutorRead, summary="Obtener un Tutor por ID (Admin)")
def get_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido por token de Admin
):
    """Obtiene los detalles de un tutor específico por su ID."""
    print(f"DEBUG REBUILD ENDPOINT: GET /{id_tutor} called.")
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    return tutor

@router.post("/", response_model=TutorRead, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo Tutor (Admin)")
def create_tutor(
    data: TutorCreate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido por token de Admin
):
    """Crea un nuevo registro de tutor."""
    print("DEBUG REBUILD ENDPOINT: POST / called.")
    return tutor_service.create_tutor(db=session, data=data)

@router.put("/{id_tutor}", response_model=TutorRead, summary="Actualizar un Tutor (Admin)")
def update_tutor(
    id_tutor: int,
    data: TutorUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido por token de Admin
):
    """Actualiza la información de un tutor existente."""
    print(f"DEBUG REBUILD ENDPOINT: PUT /{id_tutor} called.")
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    return tutor_service.update_tutor(db=session, tutor=tutor, data=data)

@router.delete("/{id_tutor}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Tutor (Admin)")
def delete_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido por token de Admin
):
    """Elimina un tutor del sistema."""
    print(f"DEBUG REBUILD ENDPOINT: DELETE /{id_tutor} called.")
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")

    session.delete(tutor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- FIN DEL ARCHIVO ---