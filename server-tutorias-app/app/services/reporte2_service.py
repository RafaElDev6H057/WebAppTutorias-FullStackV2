"""
Servicio de lógica de negocio para la gestión de Reportes Generales 2 (Finales).

Proporciona funciones para operaciones CRUD de reportes finales de proyectos de tutores.
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

from app.models.reporte2 import Reporte2
from app.schemas.reporte2 import Reporte2Create, Reporte2Update


def create_reporte2(db: Session, data: Reporte2Create, tutor_id: int) -> Reporte2:
    """
    Crea un nuevo Reporte General 2 (Final) asociándolo al tutor autenticado.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del reporte a crear.
        tutor_id: ID del tutor que crea el reporte.
    
    Returns:
        Instancia del reporte creado.
    """
    reporte_data = data.model_dump()
    nuevo_reporte = Reporte2(**reporte_data, id_tutor=tutor_id)
    
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    
    return nuevo_reporte


def get_reporte2_por_id(db: Session, reporte_id: int) -> Reporte2:
    """
    Obtiene un Reporte General 2 específico por su ID.
    """
    reporte = db.get(Reporte2, reporte_id)
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El reporte final (2) con id {reporte_id} no fue encontrado."
        )
    
    return reporte


def get_reportes2_por_tutor(db: Session, tutor_id: int) -> List[Reporte2]:
    """
    Obtiene todos los Reportes Generales 2 creados por un tutor específico.
    """
    # Ordenamos por fecha de creación descendente
    query = select(Reporte2).where(Reporte2.id_tutor == tutor_id).order_by(Reporte2.created_at.desc()) # type: ignore
    reportes = db.exec(query).all()
    
    return list(reportes)


def update_reporte2(db: Session, reporte_existente: Reporte2, data: Reporte2Update) -> Reporte2:
    """
    Actualiza un Reporte General 2 existente.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(reporte_existente, key, value)
    
    db.add(reporte_existente)
    db.commit()
    db.refresh(reporte_existente)
    
    return reporte_existente


def delete_reporte2(db: Session, reporte_existente: Reporte2) -> dict:
    """
    Elimina un Reporte General 2 existente.
    """
    db.delete(reporte_existente)
    db.commit()
    
    return {"message": f"Reporte final {reporte_existente.id} eliminado exitosamente."}