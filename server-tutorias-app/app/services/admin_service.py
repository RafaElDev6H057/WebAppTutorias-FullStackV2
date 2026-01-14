"""
Servicio de lógica de negocio para la gestión de Administradores.

Proporciona funciones para operaciones CRUD, autenticación y validación
de credenciales de administradores del sistema.
"""

from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from app.models.administrador import Administrador
from app.schemas.administrador import AdministradorCreate, AdministradorUpdate
from app.core.security import get_password_hash, verify_password


def get_admin_by_usuario(db: Session, usuario: str) -> Administrador | None:
    """
    Busca un administrador por su nombre de usuario.
    
    Args:
        db: Sesión de base de datos.
        usuario: Nombre de usuario del administrador a buscar.
    
    Returns:
        Instancia de Administrador si existe, None en caso contrario.
    """
    return db.exec(select(Administrador).where(Administrador.usuario == usuario)).first()


def authenticate_admin(db: Session, usuario: str, contraseña: str) -> Optional[Administrador]:
    """
    Autentica a un administrador validando sus credenciales.
    
    Verifica que el nombre de usuario exista y que la contraseña proporcionada
    coincida con el hash almacenado.
    
    Args:
        db: Sesión de base de datos.
        usuario: Nombre de usuario del administrador.
        contraseña: Contraseña en texto plano a validar.
    
    Returns:
        Instancia de Administrador si la autenticación es exitosa, None en caso contrario.
    """
    admin = db.exec(select(Administrador).where(Administrador.usuario == usuario)).first()
    
    if not admin:
        return None
    
    if not verify_password(contraseña, admin.contraseña):
        return None
    
    return admin


def create_admin(db: Session, data: AdministradorCreate) -> Administrador:
    """
    Crea un nuevo administrador en el sistema.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del administrador a crear.
    
    Returns:
        Instancia del administrador creado.
    
    Raises:
        HTTPException: Si el nombre de usuario ya está en uso.
    """
    db_admin = db.exec(select(Administrador).where(Administrador.usuario == data.usuario)).first()
    
    if db_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya está en uso."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    admin = Administrador.model_validate(data.model_dump(), update={'contraseña': hashed_password})
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin


def update_admin(db: Session, admin: Administrador, data: AdministradorUpdate) -> Administrador:
    """
    Actualiza los datos de un administrador existente.
    
    Si se proporciona una nueva contraseña, esta será hasheada antes de guardarse.
    
    Args:
        db: Sesión de base de datos.
        admin: Instancia del administrador a actualizar.
        data: Datos actualizados del administrador.
    
    Returns:
        Instancia del administrador actualizado.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    if "contraseña" in update_data and update_data["contraseña"]:
        update_data["contraseña"] = get_password_hash(update_data["contraseña"])
    
    for key, value in update_data.items():
        setattr(admin, key, value)
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin
