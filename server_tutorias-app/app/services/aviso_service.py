# app/services/aviso_service.py

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.aviso import Aviso
from app.schemas.aviso import AvisoCreate, AvisoUpdate

def get_aviso(db: Session, aviso_id: int) -> Aviso:
    """
    Obtiene un aviso específico por su ID.
    Lanza un error 404 si no se encuentra.
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
    Obtiene todos los avisos ACTIVOS (publicados) para los alumnos,
    ordenados del más reciente al más antiguo.
    """
    query = select(Aviso).where(Aviso.is_activo == True).order_by(Aviso.created_at.desc()) # type: ignore
    avisos = db.exec(query).all()
    
    # ✅ Convertimos a list() para satisfacer al linter
    return list(avisos) 

def get_avisos_todos(db: Session) -> List[Aviso]:
    """
    Obtiene TODOS los avisos (activos e inactivos) para el panel de admin,
    ordenados del más reciente al más antiguo.
    """
    query = select(Aviso).order_by(Aviso.created_at.desc()) # type: ignore
    avisos = db.exec(query).all()
    
    # ✅ Convertimos a list() para satisfacer al linter
    return list(avisos)

def create_aviso(db: Session, data: AvisoCreate) -> Aviso:
    """
    Crea un nuevo aviso en la base de datos.
    """
    nuevo_aviso = Aviso.model_validate(data)
    
    db.add(nuevo_aviso)
    db.commit()
    db.refresh(nuevo_aviso)
    return nuevo_aviso

def update_aviso(db: Session, aviso_id: int, data: AvisoUpdate) -> Aviso:
    """
    Actualiza un aviso existente.
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
    Elimina un aviso existente.
    """
    aviso_a_eliminar = get_aviso(db, aviso_id)
    
    db.delete(aviso_a_eliminar)
    db.commit()
    
    return {"message": f"Aviso {aviso_id} eliminado exitosamente."}