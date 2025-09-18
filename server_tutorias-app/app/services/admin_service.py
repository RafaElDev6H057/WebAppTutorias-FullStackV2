# app/services/admin_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.administrador import Administrador
from app.schemas.administrador import AdministradorCreate, AdministradorUpdate

# Pro Tip: Estas funciones de contraseña se repiten en cada servicio.
# Una mejora final sería crear un archivo `app/core/security.py`
# y ponerlas ahí para importarlas desde un único lugar.
from app.services.alumno_service import get_password_hash, verify_password


def get_admin_by_usuario(db: Session, usuario: str) -> Administrador | None:
    """Busca un administrador por su nombre de usuario."""
    return db.exec(select(Administrador).where(Administrador.usuario == usuario)).first()

def create_admin(db: Session, data: AdministradorCreate) -> Administrador:
    """Crea un nuevo administrador en la base de datos."""
    # 1. Verificamos si ya existe un admin con ese usuario
    db_admin = get_admin_by_usuario(db, data.usuario)
    if db_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El nombre de usuario '{data.usuario}' ya está en uso."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    
    # Usamos el patrón consistente para crear el objeto del modelo
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