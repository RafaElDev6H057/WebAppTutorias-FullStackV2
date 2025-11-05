"""
Servicio de lógica de negocio para la gestión de Reportes Integrales.

Proporciona funciones para operaciones CRUD con validación dinámica basada
en la etapa de configuración del sistema (filtrado de campos según etapa 1, 2 o 3).
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional

from app.models.reporte_integral import ReporteIntegral
from app.models.tutoria import Tutoria
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralUpdate
from app.services import configuracion_service


def create_or_update_reporte(db: Session, data: ReporteIntegralCreate) -> ReporteIntegral:
    """
    Crea o actualiza un reporte integral con filtrado dinámico de campos por etapa.
    
    El sistema valida la etapa actual de configuración y filtra automáticamente
    los campos que no están permitidos para esa etapa:
    - Etapa 1: Solo seguimiento_1
    - Etapa 2: seguimiento_1 y seguimiento_2
    - Etapa 3: Todos los campos habilitados
    
    También actualiza la bandera reporte_integral_guardado en la tutoría cuando
    se completa el reporte en etapa 3.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del reporte a crear o actualizar.
    
    Returns:
        Instancia del reporte creado o actualizado.
    
    Raises:
        HTTPException: Si la tutoría asociada no existe.
    """
    config = configuracion_service.get_configuracion(db)
    etapa_actual = config.reporte_integral_etapa
    
    update_data = data.model_dump()
    
    campos_etapa_3 = {
        "seguimiento_3", "tutoria_grupal", "tutoria_individual",
        "jefatura_academica", "ciencias_basicas", "psicologia",
        "materias_aprobadas", "materias_no_aprobadas"
    }
    
    campos_etapa_2 = {"seguimiento_2"}
    
    if etapa_actual == 1:
        for key in list(update_data.keys()):
            if key in campos_etapa_2 or key in campos_etapa_3:
                update_data.pop(key, None)
    
    elif etapa_actual == 2:
        for key in list(update_data.keys()):
            if key in campos_etapa_3:
                update_data.pop(key, None)
    
    tutoria_asociada = db.get(Tutoria, data.id_tutoria)
    
    if not tutoria_asociada:
        raise HTTPException(status_code=404, detail=f"Tutoría {data.id_tutoria} no encontrada.")
    
    existing_report = db.exec(
        select(ReporteIntegral).where(ReporteIntegral.id_tutoria == data.id_tutoria)
    ).first()
    
    reporte_resultante: ReporteIntegral
    
    if existing_report:
        for key, value in update_data.items():
            if key != 'id_tutoria':
                setattr(existing_report, key, value)
        db.add(existing_report)
        reporte_resultante = existing_report
    else:
        new_report = ReporteIntegral.model_validate(update_data)
        db.add(new_report)
        reporte_resultante = new_report
    
    if etapa_actual == 3 and not tutoria_asociada.reporte_integral_guardado:
        tutoria_asociada.reporte_integral_guardado = True
        db.add(tutoria_asociada)
    
    db.commit()
    db.refresh(reporte_resultante)
    
    return reporte_resultante


def get_reporte(db: Session, reporte_id: int) -> Optional[ReporteIntegral]:
    """
    Obtiene un reporte integral por su ID.
    
    Args:
        db: Sesión de base de datos.
        reporte_id: Identificador del reporte.
    
    Returns:
        Instancia del reporte encontrado.
    
    Raises:
        HTTPException: Si el reporte no existe.
    """
    reporte = db.get(ReporteIntegral, reporte_id)
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado."
        )
    
    return reporte


def get_reporte_by_tutoria(db: Session, id_tutoria: int) -> Optional[ReporteIntegral]:
    """
    Obtiene el reporte integral asociado a una tutoría específica.
    
    Args:
        db: Sesión de base de datos.
        id_tutoria: Identificador de la tutoría.
    
    Returns:
        Instancia del reporte si existe, None en caso contrario.
    """
    reporte = db.exec(
        select(ReporteIntegral).where(ReporteIntegral.id_tutoria == id_tutoria)
    ).first()
    
    return reporte


def update_reporte(
    db: Session,
    reporte_id: int,
    data: ReporteIntegralUpdate
) -> ReporteIntegral:
    """
    Actualiza un reporte integral existente.
    
    Args:
        db: Sesión de base de datos.
        reporte_id: Identificador del reporte a actualizar.
        data: Datos actualizados del reporte.
    
    Returns:
        Instancia del reporte actualizado.
    
    Raises:
        HTTPException: Si el reporte no existe.
    """
    reporte_to_update = db.get(ReporteIntegral, reporte_id)
    
    if not reporte_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado para actualizar."
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(reporte_to_update, key, value)
    
    db.add(reporte_to_update)
    db.commit()
    db.refresh(reporte_to_update)
    
    return reporte_to_update


def delete_reporte(db: Session, reporte_id: int) -> dict:
    """
    Elimina un reporte integral y actualiza la bandera en la tutoría asociada.
    
    Args:
        db: Sesión de base de datos.
        reporte_id: Identificador del reporte a eliminar.
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el reporte no existe.
    """
    reporte_to_delete = db.get(ReporteIntegral, reporte_id)
    
    if not reporte_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado para eliminar."
        )
    
    id_tutoria_asociada = reporte_to_delete.id_tutoria
    
    db.delete(reporte_to_delete)
    
    tutoria_asociada = db.get(Tutoria, id_tutoria_asociada)
    
    if tutoria_asociada:
        tutoria_asociada.reporte_integral_guardado = False
        db.add(tutoria_asociada)
    
    db.commit()
    
    return {"message": f"Reporte Integral {reporte_id} eliminado exitosamente."}
