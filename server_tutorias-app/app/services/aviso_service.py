"""
Servicio de lógica de negocio para la gestión de Avisos.

Proporciona funciones para operaciones CRUD de avisos, con distinción
entre avisos públicos (para alumnos) y todos los avisos (para administradores).
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

from app.models.aviso import Aviso
from app.schemas.aviso import AvisoCreate, AvisoUpdate


def get_aviso(db: Session, aviso_id: int) -> Aviso:
    """
    Obtiene un aviso específico por su ID.
    
    Args:
        db: Sesión de base de datos.
        aviso_id: Identificador del aviso a buscar.
    
    Returns:
        Instancia del aviso encontrado.
    
    Raises:
        HTTPException: Si el aviso no existe.
    """
    aviso = db.get(Aviso, aviso_id)
    
    if not aviso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El aviso con id {aviso_id} no fue encontrado."
        )
    
    return aviso


def get_avisos_publicos(db: Session) -> List[Aviso]:
    """
    Obtiene todos los avisos activos (publicados) para los alumnos.
    
    Args:
        db: Sesión de base de datos.
    
    Returns:
        Lista de avisos activos ordenados del más reciente al más antiguo.
    """
    query = select(Aviso).where(Aviso.is_activo == True).order_by(Aviso.created_at.desc()) #type:ignore
    avisos = db.exec(query).all()
    
    return list(avisos)


def get_avisos_todos(db: Session) -> List[Aviso]:
    """
    Obtiene todos los avisos (activos e inactivos) para el panel de administración.
    
    Args:
        db: Sesión de base de datos.
    
    Returns:
        Lista de todos los avisos ordenados del más reciente al más antiguo.
    """
    query = select(Aviso).order_by(Aviso.created_at.desc()) #type:ignore
    avisos = db.exec(query).all()
    
    return list(avisos)


def create_aviso(db: Session, data: AvisoCreate) -> Aviso:
    """
    Crea un nuevo aviso en el sistema.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del aviso a crear.
    
    Returns:
        Instancia del aviso creado.
    """
    nuevo_aviso = Aviso.model_validate(data)
    
    db.add(nuevo_aviso)
    db.commit()
    db.refresh(nuevo_aviso)
    
    return nuevo_aviso


def update_aviso(db: Session, aviso_id: int, data: AvisoUpdate) -> Aviso:
    """
    Actualiza un aviso existente.
    
    Args:
        db: Sesión de base de datos.
        aviso_id: Identificador del aviso a actualizar.
        data: Datos actualizados del aviso.
    
    Returns:
        Instancia del aviso actualizado.
    
    Raises:
        HTTPException: Si el aviso no existe.
    """
    aviso_a_actualizar = get_aviso(db, aviso_id)
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(aviso_a_actualizar, key, value)
    
    db.add(aviso_a_actualizar)
    db.commit()
    db.refresh(aviso_a_actualizar)
    
    return aviso_a_actualizar


def delete_aviso(db: Session, aviso_id: int) -> dict:
    """
    Elimina un aviso del sistema.
    
    Args:
        db: Sesión de base de datos.
        aviso_id: Identificador del aviso a eliminar.
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el aviso no existe.
    """
    aviso_a_eliminar = get_aviso(db, aviso_id)
    
    db.delete(aviso_a_eliminar)
    db.commit()
    
    return {"message": f"Aviso {aviso_id} eliminado exitosamente."}
