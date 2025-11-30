from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import Any

# Dependencias del proyecto
from app.database import get_session
from app.core.dependencies import get_current_admin_user
from app.models.administrador import Administrador

# Importamos los servicios (ahora son 3)
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
@router.get("/psicologia/{periodo}", response_class=StreamingResponse)
def descargar_reporte_psicologia(
    periodo: str,
    current_admin: Administrador = Depends(get_current_admin_user),
    db: Session = Depends(get_session)
) -> Any:
    """
    Genera y descarga el reporte Excel de alumnos canalizados a **Psicología**.
    """
    excel_file = generate_reporte_psicologia(db, periodo)
    filename = f"Canalizacion_Psicologia_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- CIENCIAS BÁSICAS ---
@router.get("/ciencias-basicas/{periodo}", response_class=StreamingResponse)
def descargar_reporte_ciencias(
    periodo: str,
    current_admin: Administrador = Depends(get_current_admin_user),
    db: Session = Depends(get_session)
) -> Any:
    """
    Genera y descarga el reporte Excel de alumnos canalizados a **Ciencias Básicas**.
    """
    excel_file = generate_reporte_ciencias_basicas(db, periodo)
    filename = f"Canalizacion_CienciasBasicas_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- JEFATURA ACADÉMICA ---
@router.get("/jefatura-academica/{periodo}", response_class=StreamingResponse)
def descargar_reporte_jefatura(
    periodo: str,
    current_admin: Administrador = Depends(get_current_admin_user),
    db: Session = Depends(get_session)
) -> Any:
    """
    Genera y descarga el reporte Excel de alumnos canalizados a **Jefatura Académica**.
    """
    excel_file = generate_reporte_jefatura_academica(db, periodo)
    filename = f"Canalizacion_JefaturaAcademica_{periodo}.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return StreamingResponse(
        excel_file, 
        headers=headers, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )