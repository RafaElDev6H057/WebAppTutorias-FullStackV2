from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import Any

# Dependencias del proyecto
from app.database import get_session
from app.core.dependencies import get_admin_cualquier_rol
from app.models.administrador import Administrador, RolAdministrador

# Importamos los servicios
from app.services.canalizacion_service import (
    generate_reporte_psicologia,
    generate_reporte_ciencias_basicas,
    generate_reporte_jefatura_academica
)

router = APIRouter(
    prefix="/canalizaciones",
    tags=["Canalizaciones"],
    responses={404: {"description": "Not found"}},
)

# --- PSICOLOGÍA ---
@router.get(
    "/psicologia/{periodo}", 
    response_class=StreamingResponse,
    summary="Descargar Reporte Psicología",
    description="Genera el reporte de alumnos canalizados a **Psicología**.\n\n**Requiere Rol:** SUPER_ADMIN o PSICOLOGIA.",
    responses={
        403: {
            "description": "Permisos Insuficientes",
            "content": {
                "application/json": {
                    "example": {"detail": "No tienes permisos para acceder a los reportes de Psicología."}
                }
            }
        }
    }
)
def descargar_reporte_psicologia(
    periodo: str,
    current_admin: Administrador = Depends(get_admin_cualquier_rol),
    db: Session = Depends(get_session)
) -> Any:
    # Validación de Rol Específica
    if current_admin.rol not in [RolAdministrador.SUPER_ADMIN, RolAdministrador.PSICOLOGIA]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a los reportes de Psicología."
        )

    excel_file = generate_reporte_psicologia(db, periodo)
    filename = f"Canalizacion_Psicologia_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- CIENCIAS BÁSICAS ---
@router.get(
    "/ciencias-basicas/{periodo}", 
    response_class=StreamingResponse,
    summary="Descargar Reporte Ciencias Básicas",
    description="Genera el reporte de alumnos canalizados a **Ciencias Básicas**.\n\n**Requiere Rol:** SUPER_ADMIN o CIENCIAS_BASICAS.",
    responses={
        403: {
            "description": "Permisos Insuficientes",
            "content": {
                "application/json": {
                    "example": {"detail": "No tienes permisos para acceder a los reportes de Ciencias Básicas."}
                }
            }
        }
    }
)
def descargar_reporte_ciencias(
    periodo: str,
    current_admin: Administrador = Depends(get_admin_cualquier_rol),
    db: Session = Depends(get_session)
) -> Any:
    # Validación de Rol Específica
    if current_admin.rol not in [RolAdministrador.SUPER_ADMIN, RolAdministrador.CIENCIAS_BASICAS]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a los reportes de Ciencias Básicas."
        )

    excel_file = generate_reporte_ciencias_basicas(db, periodo)
    filename = f"Canalizacion_CienciasBasicas_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- JEFATURA ACADÉMICA ---
@router.get(
    "/jefatura-academica/{periodo}", 
    response_class=StreamingResponse,
    summary="Descargar Reporte Jefatura Académica",
    description="Genera el reporte de alumnos canalizados a **Jefatura Académica**.\n\n**Requiere Rol:** SUPER_ADMIN o JEFATURA_ACADEMICA.",
    responses={
        403: {
            "description": "Permisos Insuficientes",
            "content": {
                "application/json": {
                    "example": {"detail": "No tienes permisos para acceder a los reportes de Jefatura Académica."}
                }
            }
        }
    }
)
def descargar_reporte_jefatura(
    periodo: str,
    current_admin: Administrador = Depends(get_admin_cualquier_rol),
    db: Session = Depends(get_session)
) -> Any:
    # Validación de Rol Específica
    if current_admin.rol not in [RolAdministrador.SUPER_ADMIN, RolAdministrador.JEFATURA_ACADEMICA]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a los reportes de Jefatura Académica."
        )

    excel_file = generate_reporte_jefatura_academica(db, periodo)
    filename = f"Canalizacion_JefaturaAcademica_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )