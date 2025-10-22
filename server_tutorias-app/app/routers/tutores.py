# app/routers/tutores.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List
from datetime import timedelta

# ⚙️ Imports refactorizados
from app.database import get_session
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate, TutorRead
from app.schemas.administrador import Token # Reutilizamos el esquema del token
from app.services import tutor_service
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

# 👇 Importamos la dependencia de Admin para proteger el CRUD
from app.core.dependencies import get_current_admin_user
from app.models.administrador import Administrador # Importamos el modelo para type hinting

router = APIRouter(prefix="/tutores", tags=["Tutores"])

# --- Esquema de autenticación para Tutores ---
oauth2_scheme_tutor = OAuth2PasswordBearer(tokenUrl="/api/tutores/login")


# --- Endpoint de Login para Tutores ---
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

    # --- LÓGICA DE LOGIN DUAL ---
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
    
    # Creamos el token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        # Guardamos el 'id_tutor' en el token para identificarlo
        data={"sub": str(tutor.id_tutor), "role": "tutor"}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# --- Endpoints de Gestión (CRUD para Admins) ---

# 🔹 Obtener todos los tutores (PROTEGIDO)
@router.get("/", response_model=List[TutorRead], summary="Obtener todos los Tutores (Admin)")
def get_tutores(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # 👈 Protegido
):
    return session.exec(select(Tutor)).all()


# 🔹 Obtener tutor por ID (PROTEGIDO)
@router.get("/{id_tutor}", response_model=TutorRead, summary="Obtener un Tutor por ID (Admin)")
def get_tutor(
    id_tutor: int, 
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # 👈 Protegido
):
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    return tutor


# 🔹 Crear tutor (PROTEGIDO)
@router.post("/", response_model=TutorRead, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo Tutor (Admin)")
def create_tutor(
    data: TutorCreate, 
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # 👈 Protegido
):
    return tutor_service.create_tutor(db=session, data=data)


# 🔹 Actualizar tutor (PROTEGIDO)
@router.put("/{id_tutor}", response_model=TutorRead, summary="Actualizar un Tutor (Admin)")
def update_tutor(
    id_tutor: int,
    data: TutorUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # 👈 Protegido
):
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    return tutor_service.update_tutor(db=session, tutor=tutor, data=data)


# 🔹 Eliminar tutor (PROTEGIDO)
@router.delete("/{id_tutor}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Tutor (Admin)")
def delete_tutor(
    id_tutor: int, 
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # 👈 Protegido
):
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    session.delete(tutor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)