# app/services/admin_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from app.models.administrador import Administrador
from app.schemas.administrador import AdministradorCreate, AdministradorUpdate
from app.core.security import get_password_hash, verify_password


def get_admin_by_usuario(db: Session, usuario: str) -> Administrador | None:
    """Busca un administrador por su nombre de usuario."""
    return db.exec(select(Administrador).where(Administrador.usuario == usuario)).first()

def authenticate_admin(db: Session, usuario: str, contraseña: str) -> Optional[Administrador]:
    """
    Autentica a un administrador. Devuelve el objeto del admin si es exitoso, si no, None.
    """
    admin = db.exec(select(Administrador).where(Administrador.usuario == usuario)).first()
    if not admin:
        return None
    if not verify_password(contraseña, admin.contraseña):
        return None
    return admin

def create_admin(db: Session, data: AdministradorCreate) -> Administrador:
    """Crea un nuevo administrador en la base de datos."""
    db_admin = db.exec(select(Administrador).where(Administrador.usuario == data.usuario)).first()
    if db_admin:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya está en uso.")
    
    hashed_password = get_password_hash(data.contraseña)
    admin = Administrador.model_validate(data.model_dump(), update={'contraseña': hashed_password})
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def update_admin(db: Session, admin: Administrador, data: AdministradorUpdate) -> Administrador:
    """Actualiza los datos de un administrador."""
    update_data = data.model_dump(exclude_unset=True)

    # Si la contraseña está en los datos para actualizar, la hasheamos
    if "contraseña" in update_data and update_data["contraseña"]:
        update_data["contraseña"] = get_password_hash(update_data["contraseña"])
    
    for key, value in update_data.items():
        setattr(admin, key, value)
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin