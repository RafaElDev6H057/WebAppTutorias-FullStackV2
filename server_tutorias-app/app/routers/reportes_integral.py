from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import Union
import io

from app.database import get_session
from app.models.reporte_integral import ReporteIntegral
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralRead, ReporteIntegralUpdate
from app.services import reporte_integral_service, pdf_generator_service
from app.core.dependencies import get_current_user
from app.models.administrador import Administrador
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria

# Prefijo específico para este módulo
router = APIRouter(prefix="/reportes/integral", tags=["Reporte Integral"])


@router.post(
    "", # Se mapea a POST /reportes/integral
    response_model=ReporteIntegralRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear o Actualizar Reporte Integral"
)
def handle_create_or_update_reporte(
    data: ReporteIntegralCreate,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Crea o actualiza un reporte integral (operación upsert).
    """
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, data.id_tutoria)
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para crear/modificar un reporte para esta tutoría."
            )
    
    reporte = reporte_integral_service.create_or_update_reporte(db=session, data=data)
    return reporte


@router.get(
    "/tutoria/{id_tutoria}",
    response_model=ReporteIntegralRead,
    summary="Obtener Reporte Integral por ID de Tutoría"
)
def handle_get_reporte_by_tutoria(
    id_tutoria: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene el reporte integral asociado a una tutoría específica.
    """
    reporte = reporte_integral_service.get_reporte_by_tutoria(db=session, id_tutoria=id_tutoria)
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte Integral no encontrado para esta tutoría."
        )
    
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, id_tutoria)
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este reporte."
            )
    
    return reporte


@router.get(
    "/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Obtener Reporte Integral por ID"
)
def handle_get_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, reporte.id_tutoria) #type: ignore
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso."
            )
    
    return reporte


@router.put(
    "/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Actualizar Reporte Integral"
)
def handle_update_reporte(
    reporte_id: int,
    data: ReporteIntegralUpdate,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, reporte_existente.id_tutoria) #type: ignore
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso."
            )
    
    reporte_actualizado = reporte_integral_service.update_reporte(
        db=session, reporte_id=reporte_id, data=data
    )
    
    return reporte_actualizado


@router.delete(
    "/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Reporte Integral"
)
def handle_delete_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, reporte_existente.id_tutoria) #type: ignore
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso."
            )
    
    reporte_integral_service.delete_reporte(db=session, reporte_id=reporte_id)
    return


@router.get(
    "/pdf/tutor/{id_tutor}/periodo/{periodo}",
    summary="Generar PDF del Reporte Integral por Tutor y Periodo",
    response_class=StreamingResponse
)
async def handle_generate_integral_pdf(
    id_tutor: int,
    periodo: str,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    if isinstance(current_user, Tutor) and current_user.id_tutor != id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para generar este reporte."
        )
    
    try:
        pdf_stream: io.BytesIO = pdf_generator_service.generate_integral_report_pdf(
            db=session, id_tutor=id_tutor, periodo=periodo
        )
        
        filename = f"Reporte_Integral_Tutor_{id_tutor}_{periodo}.pdf"
        
        return StreamingResponse(
            content=pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al generar el PDF."
        )