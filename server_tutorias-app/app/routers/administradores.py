# app/routers/administradores.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import timedelta
from jose import JWTError, jwt

from app.database import get_session
from app.models.administrador import Administrador
from app.schemas.administrador import (
    AdministradorCreate, 
    AdministradorRead, 
    AdministradorUpdate, 
    Token, 
    TokenData
)
from app.services import admin_service
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/administradores", tags=["Administradores"])

# ✅ LA CORRECCIÓN: La ruta es relativa al prefijo del router.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/administradores/login")


# --- DEPENDENCIA PARA PROTEGER RUTAS ---
def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> Administrador:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: Optional[str] = payload.get("sub")
        if usuario is None:
            raise credentials_exception
        token_data = TokenData(usuario=usuario)
    except JWTError:
        raise credentials_exception
    
    user = admin_service.get_admin_by_usuario(db, usuario=token_data.usuario) # type:ignore
    if user is None:
        raise credentials_exception
    return user


# --- ENDPOINTS ---

# 🔹 POST /login - AHORA DEVUELVE UN TOKEN
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_session)
):
    admin = admin_service.authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": admin.usuario}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# 🔹 GET / - OBTENER TODOS LOS ADMINS (PROTEGIDO)
@router.get("/", response_model=List[AdministradorRead])
def get_all_admins(
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(Administrador)).all()


# 🔹 GET /{id_admin} - OBTENER UN ADMIN POR ID (PROTEGIDO)
@router.get("/{id_admin}", response_model=AdministradorRead)
def get_admin_by_id(
    id_admin: int,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    admin = session.get(Administrador, id_admin)
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return admin


# 🔹 POST / - CREAR UN NUEVO ADMIN (PROTEGIDO)
@router.post("/", response_model=AdministradorRead, status_code=status.HTTP_201_CREATED)
def create_admin(
    data: AdministradorCreate,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    return admin_service.create_admin(db=session, data=data)


# 🔹 PUT /{id_admin} - ACTUALIZAR UN ADMIN (PROTEGIDO)
@router.put("/{id_admin}", response_model=AdministradorRead)
def update_admin(
    id_admin: int,
    data: AdministradorUpdate,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    admin_to_update = session.get(Administrador, id_admin)
    if not admin_to_update:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    return admin_service.update_admin(db=session, admin=admin_to_update, data=data)


# 🔹 DELETE /{id_admin} - ELIMINAR UN ADMIN (PROTEGIDO)
@router.delete("/{id_admin}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    id_admin: int,
    current_admin: Administrador = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    admin_to_delete = session.get(Administrador, id_admin)
    if not admin_to_delete:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    session.delete(admin_to_delete)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)