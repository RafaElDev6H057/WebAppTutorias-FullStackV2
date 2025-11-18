# app/routers/configuracion.py

"""
Endpoints de la API para gestión de Configuración del Sistema.

Proporciona endpoints para consultar y actualizar la configuración global
que controla las etapas habilitadas del reporte integral de tutorías.
"""
import shutil
import os

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlmodel import Session
from typing import Union

from app.database import get_session
from app.services import configuracion_service
from app.schemas.configuracion import ConfiguracionRead, ConfiguracionUpdate
from app.core.dependencies import get_current_admin_user, get_current_user
from app.models.administrador import Administrador
from app.models.tutor import Tutor

# --- Rutas de Plantillas ---
TEMPLATE_DIR = "app/pdf_templates"
TEMPLATE_INTEGRAL_PATH = f"{TEMPLATE_DIR}/formato.pdf"
TEMPLATE_INTEGRAL_ORIGINAL_PATH = f"{TEMPLATE_DIR}/formato_original.pdf" # 👈 La copia maestra

router = APIRouter(prefix="/configuracion", tags=["Configuración"])


@router.get("/", response_model=ConfiguracionRead, summary="Obtener etapa actual del reporte")
def get_reporte_config(
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene la configuración actual del sistema.
    
    Retorna la etapa habilitada del reporte integral de tutorías:
    - Etapa 1: Solo Seguimiento 1
    - Etapa 2: Seguimiento 1 y 2
    - Etapa 3: Reporte completo (todas las secciones)
    
    Accesible por administradores y tutores autenticados.
    
    Returns:
        Configuración actual con la etapa activa.
    """
    config = configuracion_service.get_configuracion(db=session)
    return config


@router.put("/", response_model=ConfiguracionRead, summary="Actualizar etapa del reporte (Solo Admin)")
def update_reporte_config(
    data: ConfiguracionUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Actualiza la etapa habilitada del reporte integral.
    
    Permite cambiar la etapa actual del proceso de llenado del reporte:
    - 1: Solo permite Seguimiento 1
    - 2: Permite Seguimiento 1 y 2
    - 3: Habilita el reporte completo
    
    Solo accesible por administradores.
    
    Returns:
        Configuración actualizada con la nueva etapa.
    """
    config = configuracion_service.update_configuracion(db=session, data=data)
    return config


@router.post(
    "/upload-template/integral",
    summary="Actualizar plantilla del Reporte Integral (Admin)",
    status_code=status.HTTP_200_OK
)
async def update_integral_template(
    file: UploadFile = File(..., description="Nuevo archivo PDF de plantilla"),
    current_admin: Administrador = Depends(get_current_admin_user) # Solo Admin
):
    """
    Permite reemplazar el archivo 'formato.pdf' del Reporte Integral.
    Útil para actualizar logos o textos estáticos.
    
    **ADVERTENCIA:** El nuevo PDF debe mantener la misma estructura de filas/celdas,
    o los datos se imprimirán desalineados.
    """
    
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    try:
        # Sobrescribir el archivo con el nuevo
        with open(TEMPLATE_INTEGRAL_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"message": "Plantilla actualizada exitosamente. El sistema ahora usará el nuevo formato."}

    except Exception as e:
        print(f"Error al actualizar plantilla: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al guardar el archivo. Verifica permisos de escritura en el servidor."
        )


# ✅ NUEVO ENDPOINT DE RESTAURACIÓN
@router.post(
    "/reset-template/integral",
    summary="Restaurar plantilla original del Reporte Integral (Admin)",
    status_code=status.HTTP_200_OK
)
async def reset_integral_template(
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Restaura el archivo 'formato.pdf' copiando desde 'formato_original.pdf'.
    Útil si la plantilla subida tiene errores o se quiere volver al defecto.
    """
    if not os.path.exists(TEMPLATE_INTEGRAL_ORIGINAL_PATH):
        raise HTTPException(
            status_code=500, 
            detail="No se encontró el archivo de plantilla original en el servidor. Contacte al soporte técnico."
        )

    try:
        # Copiar el original sobre el activo, sobrescribiéndolo
        shutil.copy2(TEMPLATE_INTEGRAL_ORIGINAL_PATH, TEMPLATE_INTEGRAL_PATH)
        return {"message": "Plantilla restaurada a su versión original por defecto exitosamente."}

    except Exception as e:
        print(f"Error al restaurar plantilla: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al restaurar la plantilla."
        )