from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import List, Union
import io

from app.database import get_session
from app.models.reporte2 import Reporte2
from app.schemas.reporte2 import Reporte2Create, Reporte2Read, Reporte2Update
from app.services import reporte2_service, pdf_generator_service # <--- Importamos el generador de PDF
from app.core.dependencies import get_current_user, get_current_tutor_user, oauth2_scheme_tutor
from app.models.administrador import Administrador
from app.models.tutor import Tutor

router = APIRouter(prefix="/reportes/general-2", tags=["Reporte General 2"])


@router.post(
    "",
    response_model=Reporte2Read,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Reporte General 2 (Final)",
    dependencies=[Depends(oauth2_scheme_tutor)]
)
def handle_create_reporte2(
    data: Reporte2Create,
    session: Session = Depends(get_session),
    current_tutor: Tutor = Depends(get_current_tutor_user)
):
    """
    Crea el Reporte Final de un proyecto.
    """
    reporte2 = reporte2_service.create_reporte2(db=session, data=data, tutor_id=current_tutor.id_tutor) #type: ignore
    return reporte2


@router.get(
    "/tutor",
    response_model=List[Reporte2Read],
    summary="Obtener todos los Reportes 2 del Tutor autenticado",
    dependencies=[Depends(oauth2_scheme_tutor)]
)
def handle_get_reportes2_por_tutor(
    session: Session = Depends(get_session),
    current_tutor: Tutor = Depends(get_current_tutor_user)
):
    reportes = reporte2_service.get_reportes2_por_tutor(db=session, tutor_id=current_tutor.id_tutor) #type: ignore
    return reportes


@router.get(
    "/{reporte_id}",
    response_model=Reporte2Read,
    summary="Obtener un Reporte 2 específico por ID"
)
def handle_get_reporte2_por_id(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte = reporte2_service.get_reporte2_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este reporte."
        )
    
    return reporte


@router.put(
    "/{reporte_id}",
    response_model=Reporte2Read,
    summary="Actualizar un Reporte 2"
)
def handle_update_reporte2(
    reporte_id: int,
    data: Reporte2Update,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte2_service.get_reporte2_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte_existente.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este reporte."
        )
    
    reporte_actualizado = reporte2_service.update_reporte2(
        db=session, reporte_existente=reporte_existente, data=data
    )
    
    return reporte_actualizado


@router.delete(
    "/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un Reporte 2"
)
def handle_delete_reporte2(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte2_service.get_reporte2_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte_existente.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este reporte."
        )
    
    reporte2_service.delete_reporte2(db=session, reporte_existente=reporte_existente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- NUEVO ENDPOINT PDF ---
@router.get(
    "/{reporte_id}/pdf",
    response_class=StreamingResponse,
    summary="Descargar Reporte 2 en PDF"
)
async def handle_generate_reporte2_pdf(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Genera y descarga el PDF del Reporte General 2 (Final).
    """
    reporte = reporte2_service.get_reporte2_por_id(db=session, reporte_id=reporte_id)
    
    # Validar permisos
    if isinstance(current_user, Tutor) and reporte.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para generar este reporte."
        )
    
    try:
        # Llamamos al nuevo servicio que creamos
        pdf_stream: io.BytesIO = pdf_generator_service.generate_reporte2_pdf(
            db=session, reporte_id=reporte_id
        )
        
        # Nombre del archivo limpio
        proyecto_name = reporte.nombre_proyecto[:20] if len(reporte.nombre_proyecto) > 20 else reporte.nombre_proyecto
        filename = f"Reporte_Final_{proyecto_name}_{reporte.periodo}.pdf"
        
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
        print(f"Error generando PDF Reporte 2: {e}") # Log simple para debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al generar el PDF."
        )