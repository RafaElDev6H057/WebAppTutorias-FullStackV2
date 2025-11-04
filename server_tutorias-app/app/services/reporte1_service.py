# app/services/reporte1_service.py

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

# Importamos los modelos y esquemas necesarios
from app.models.reporte1 import Reporte1
from app.schemas.reporte1 import Reporte1Create, Reporte1Update
from app.models.tutor import Tutor # Importamos Tutor para el type hint

def create_reporte1(db: Session, data: Reporte1Create, tutor_id: int) -> Reporte1:
    """
    Crea un nuevo Reporte General 1, asociándolo al tutor autenticado.
    """
    
    # Creamos una instancia del modelo Reporte1 a partir de los datos del schema
    # y añadimos el id_tutor del usuario que lo está creando.
    reporte_data = data.model_dump()
    nuevo_reporte = Reporte1(
        **reporte_data,
        id_tutor=tutor_id
    )
    
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    
    return nuevo_reporte

def get_reporte1_por_id(db: Session, reporte_id: int) -> Reporte1:
    """
    Obtiene un Reporte General 1 específico por su ID.
    Lanza 404 si no se encuentra.
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
    Obtiene todos los Reportes Generales 1 creados por un tutor específico,
    ordenados del más reciente al más antiguo.
    """
    query = select(Reporte1).where(Reporte1.id_tutor == tutor_id).order_by(Reporte1.created_at.desc()) # type: ignore
    reportes = db.exec(query).all()
    return list(reportes)

def update_reporte1(db: Session, reporte_existente: Reporte1, data: Reporte1Update) -> Reporte1:
    """
    Actualiza un Reporte General 1 existente.
    El reporte_existente ya ha sido verificado por el router (propietario).
    """
    # Obtenemos los datos del schema que sí fueron enviados (no None)
    update_data = data.model_dump(exclude_unset=True)
    
    # Actualizamos el objeto del modelo
    for key, value in update_data.items():
        setattr(reporte_existente, key, value)
        
    db.add(reporte_existente)
    db.commit()
    db.refresh(reporte_existente)
    return reporte_existente

def delete_reporte1(db: Session, reporte_existente: Reporte1) -> dict:
    """
    Elimina un Reporte General 1 existente.
    El reporte_existente ya ha sido verificado por el router (propietario).
    """
    db.delete(reporte_existente)
    db.commit()
    
    return {"message": f"Reporte {reporte_existente.id} eliminado exitosamente."}