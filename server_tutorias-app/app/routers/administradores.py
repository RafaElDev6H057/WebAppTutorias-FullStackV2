# routers/administradores.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.administrador import Administrador
from app.schemas.administrador import (
    AdministradorCreate,
    AdministradorRead,
    AdministradorUpdate,
    AdministradorLogin
)
from app.services import admin_service

router = APIRouter(prefix="/administradores", tags=["Administradores"]) # Cambiado a plural por consistencia


# ✅ 1. Dependencia reutilizable para obtener el admin o lanzar 404
def get_admin_or_404(id_admin: int, session: Session = Depends(get_session)) -> Administrador:
    admin = session.get(Administrador, id_admin)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Administrador no encontrado")
    return admin


# 🔹 GET todos
@router.get("/", response_model=List[AdministradorRead])
def get_all_admins(session: Session = Depends(get_session)):
    return session.exec(select(Administrador)).all()


# 🔹 GET por ID
@router.get("/{id_admin}", response_model=AdministradorRead)
def get_admin_by_id(admin: Administrador = Depends(get_admin_or_404)):
    return admin


# 🔹 POST crear
@router.post("/", response_model=AdministradorRead, status_code=status.HTTP_201_CREATED)
def create_admin(data: AdministradorCreate, session: Session = Depends(get_session)):
    return admin_service.create_admin(db=session, data=data)


# 🔹 PUT actualizar
@router.put("/{id_admin}", response_model=AdministradorRead)
def update_admin(
    data: AdministradorUpdate,
    admin: Administrador = Depends(get_admin_or_404),
    session: Session = Depends(get_session)
):
    return admin_service.update_admin(db=session, admin=admin, data=data)


# 🔹 DELETE eliminar
@router.delete("/{id_admin}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin: Administrador = Depends(get_admin_or_404), session: Session = Depends(get_session)):
    # ✅ 2. Respuesta estándar y correcta para eliminación
    session.delete(admin)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 🔹 POST login
@router.post("/login", response_model=AdministradorRead)
def login(data: AdministradorLogin, session: Session = Depends(get_session)):
    admin = admin_service.get_admin_by_usuario(session, data.usuario)

    if not admin or not admin_service.verify_password(data.contraseña, admin.contraseña):
        # ✅ 3. Excepción estándar para fallo de autenticación
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ✅ 4. Respuesta consistente que usa el response_model para filtrar datos
    return admin