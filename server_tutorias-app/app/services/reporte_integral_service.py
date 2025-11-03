# app/services/reporte_integral_service.py

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional # Asegúrate de que Optional esté importado

# Models
from app.models.reporte_integral import ReporteIntegral
from app.models.tutoria import Tutoria

# Schemas
# 👇 Importa el nuevo ReporteIntegralUpdate
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralUpdate
from app.services import configuracion_service

# --- Función Create/Update (Upsert) - SIN CAMBIOS ---
def create_or_update_reporte(db: Session, data: ReporteIntegralCreate) -> ReporteIntegral:
    """
    Crea o actualiza un reporte integral, VALIDANDO y FILTRANDO por la etapa actual.
    """
    # 1. Obtener la etapa actual del sistema
    config = configuracion_service.get_configuracion(db)
    etapa_actual = config.reporte_integral_etapa

    # 2. Convertir los datos de entrada a un diccionario
    # Usamos exclude_unset=False para obtener todos los campos, incluidos los defaults
    update_data = data.model_dump() 

    # 3. --- LÓGICA DE FILTRADO (EL CAMBIO) ---
    # En lugar de lanzar un error, eliminamos los campos no permitidos
    # del diccionario 'update_data' ANTES de guardar.
    
    campos_etapa_3 = {
        "seguimiento_3", "tutoria_grupal", "tutoria_individual",
        "jefatura_academica", "ciencias_basicas", "psicologia",
        "materias_aprobadas", "materias_no_aprobadas"
    }
    campos_etapa_2 = {"seguimiento_2"}

    if etapa_actual == 1:
        # Si estamos en etapa 1, eliminamos todos los campos de etapa 2 y 3
        for key in list(update_data.keys()): # Usamos list() para poder modificar el dict mientras iteramos
            if key in campos_etapa_2 or key in campos_etapa_3:
                update_data.pop(key, None) # Elimina el campo
                
    elif etapa_actual == 2:
        # Si estamos en etapa 2, eliminamos todos los campos de etapa 3
        for key in list(update_data.keys()):
            if key in campos_etapa_3:
                update_data.pop(key, None) # Elimina el campo
    
    # Si la etapa es 3, 'update_data' se queda como está, con todos los campos.

    # 4. Lógica "Upsert"
    tutoria_asociada = db.get(Tutoria, data.id_tutoria)
    if not tutoria_asociada:
        raise HTTPException(status_code=404, detail=f"Tutoría {data.id_tutoria} no encontrada.")

    existing_report = db.exec(
        select(ReporteIntegral).where(ReporteIntegral.id_tutoria == data.id_tutoria)
    ).first()

    reporte_resultante: ReporteIntegral
    if existing_report:
        # ACTUALIZAR REPORTE EXISTENTE
        # Usamos el diccionario 'update_data' ya filtrado
        for key, value in update_data.items():
            if key != 'id_tutoria': 
                setattr(existing_report, key, value)
        db.add(existing_report)
        reporte_resultante = existing_report
    else:
        # CREAR NUEVO REPORTE
        # Usamos el diccionario 'update_data' filtrado para crear el modelo
        new_report = ReporteIntegral.model_validate(update_data)
        db.add(new_report)
        reporte_resultante = new_report

    # 5. Actualizar bandera de "Guardado"
    # La bandera solo se activa cuando se guardan datos en la etapa final
    if etapa_actual == 3 and not tutoria_asociada.reporte_integral_guardado:
        tutoria_asociada.reporte_integral_guardado = True
        db.add(tutoria_asociada)

    db.commit()
    db.refresh(reporte_resultante)
    return reporte_resultante

# --- NUEVAS FUNCIONES CRUD ---

def get_reporte(db: Session, reporte_id: int) -> Optional[ReporteIntegral]:
    """Obtiene un reporte integral por su ID."""
    reporte = db.get(ReporteIntegral, reporte_id)
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado."
        )
    return reporte

def get_reporte_by_tutoria(db: Session, id_tutoria: int) -> Optional[ReporteIntegral]:
    """Obtiene el reporte integral asociado a un ID de Tutoría."""
    reporte = db.exec(
        select(ReporteIntegral).where(ReporteIntegral.id_tutoria == id_tutoria)
    ).first()
    # No lanzamos 404 aquí, permitimos que devuelva None si no existe aún
    return reporte

def update_reporte(
    db: Session,
    reporte_id: int,
    data: ReporteIntegralUpdate # Usa el nuevo esquema Update
) -> ReporteIntegral:
    """Actualiza un reporte integral existente."""
    reporte_to_update = db.get(ReporteIntegral, reporte_id)
    if not reporte_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado para actualizar."
        )

    # Obtenemos los datos del payload que sí tienen valor
    update_data = data.model_dump(exclude_unset=True)

    # Actualizamos los campos
    for key, value in update_data.items():
        setattr(reporte_to_update, key, value)

    db.add(reporte_to_update) # Marcar como modificado
    db.commit()
    db.refresh(reporte_to_update) # Devolver el objeto actualizado
    return reporte_to_update

def delete_reporte(db: Session, reporte_id: int) -> dict:
    """Elimina un reporte integral y actualiza la bandera en la Tutoría a False."""
    reporte_to_delete = db.get(ReporteIntegral, reporte_id)
    if not reporte_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte Integral con id {reporte_id} no encontrado para eliminar."
        )

    id_tutoria_asociada = reporte_to_delete.id_tutoria

    # Eliminar el reporte
    db.delete(reporte_to_delete)

    # Buscar la tutoría asociada y actualizar la bandera
    tutoria_asociada = db.get(Tutoria, id_tutoria_asociada)
    if tutoria_asociada:
        tutoria_asociada.reporte_integral_guardado = False
        db.add(tutoria_asociada) # Marcar como modificada
    else:
        # Log de advertencia si la tutoría ya no existe
        print(f"ADVERTENCIA: Se eliminó reporte {reporte_id}, pero la tutoría {id_tutoria_asociada} no se encontró.")

    db.commit() # Guardar eliminación y actualización de bandera

    return {"message": f"Reporte Integral {reporte_id} eliminado exitosamente."}