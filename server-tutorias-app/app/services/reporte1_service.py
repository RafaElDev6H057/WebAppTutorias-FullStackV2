"""
Servicio de lógica de negocio para la gestión de Reportes Generales 1.

Proporciona funciones para operaciones CRUD de reportes de proyectos de tutores,
con validación de propiedad y permisos basados en el tutor autenticado.
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

from app.models.reporte1 import Reporte1
from app.schemas.reporte1 import Reporte1Create, Reporte1Update


def create_reporte1(db: Session, data: Reporte1Create, tutor_id: int) -> Reporte1:
    """
    Crea un nuevo Reporte General 1 asociándolo al tutor autenticado.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del reporte a crear.
        tutor_id: ID del tutor que crea el reporte (obtenido del token).
    
    Returns:
        Instancia del reporte creado.
    """
    reporte_data = data.model_dump()
    nuevo_reporte = Reporte1(**reporte_data, id_tutor=tutor_id)
    
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    
    return nuevo_reporte


def get_reporte1_por_id(db: Session, reporte_id: int) -> Reporte1:
    """
    Obtiene un Reporte General 1 específico por su ID.
    
    Args:
        db: Sesión de base de datos.
        reporte_id: Identificador del reporte.
    
    Returns:
        Instancia del reporte encontrado.
    
    Raises:
        HTTPException: Si el reporte no existe.
    """
    reporte = db.get(Reporte1, reporte_id)
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El reporte con id {reporte_id} no fue encontrado."
        )
    
    return reporte


def get_reportes_por_tutor(db: Session, tutor_id: int) -> List[Reporte1]:
    """
    Obtiene todos los Reportes Generales 1 creados por un tutor específico.
    
    Args:
        db: Sesión de base de datos.
        tutor_id: ID del tutor propietario de los reportes.
    
    Returns:
        Lista de reportes ordenados del más reciente al más antiguo.
    """
    query = select(Reporte1).where(Reporte1.id_tutor == tutor_id).order_by(Reporte1.created_at.desc()) #type: ignore
    reportes = db.exec(query).all()
    
    return list(reportes)


def update_reporte1(db: Session, reporte_existente: Reporte1, data: Reporte1Update) -> Reporte1:
    """
    Actualiza un Reporte General 1 existente.
    
    El reporte debe haber sido previamente validado por el router
    para verificar permisos de propiedad.
    
    Args:
        db: Sesión de base de datos.
        reporte_existente: Instancia del reporte a actualizar.
        data: Datos actualizados del reporte.
    
    Returns:
        Instancia del reporte actualizado.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(reporte_existente, key, value)
    
    db.add(reporte_existente)
    db.commit()
    db.refresh(reporte_existente)
    
    return reporte_existente


def delete_reporte1(db: Session, reporte_existente: Reporte1) -> dict:
    """
    Elimina un Reporte General 1 existente.
    
    El reporte debe haber sido previamente validado por el router
    para verificar permisos de propiedad.
    
    Args:
        db: Sesión de base de datos.
        reporte_existente: Instancia del reporte a eliminar.
    
    Returns:
        Diccionario con mensaje de confirmación.
    """
    db.delete(reporte_existente)
    db.commit()
    
    return {"message": f"Reporte {reporte_existente.id} eliminado exitosamente."}
