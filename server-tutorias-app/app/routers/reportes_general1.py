from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import List, Union
import io

from app.database import get_session
from app.models.reporte1 import Reporte1
from app.schemas.reporte1 import Reporte1Create, Reporte1Read, Reporte1Update
from app.services import reporte1_service, pdf_generator_service
from app.core.dependencies import get_current_user, get_current_tutor_user, oauth2_scheme_tutor
from app.models.administrador import Administrador
from app.models.tutor import Tutor

router = APIRouter(prefix="/reportes/general-1", tags=["Reporte General 1"])


@router.post(
    "",
    response_model=Reporte1Read,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Reporte General 1",
    dependencies=[Depends(oauth2_scheme_tutor)]
)
def handle_create_reporte1(
    data: Reporte1Create,
    session: Session = Depends(get_session),
    current_tutor: Tutor = Depends(get_current_tutor_user)
):
    reporte1 = reporte1_service.create_reporte1(db=session, data=data, tutor_id=current_tutor.id_tutor) #type: ignore
    return reporte1


@router.get(
    "/tutor",
    response_model=List[Reporte1Read],
    summary="Obtener todos los Reportes 1 del Tutor autenticado",
    dependencies=[Depends(oauth2_scheme_tutor)]
)
def handle_get_reportes1_por_tutor(
    session: Session = Depends(get_session),
    current_tutor: Tutor = Depends(get_current_tutor_user)
):
    reportes = reporte1_service.get_reportes_por_tutor(db=session, tutor_id=current_tutor.id_tutor) #type: ignore
    return reportes


@router.get(
    "/{reporte_id}",
    response_model=Reporte1Read,
    summary="Obtener un Reporte 1 específico por ID"
)
def handle_get_reporte1_por_id(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este reporte."
        )
    
    return reporte


@router.put(
    "/{reporte_id}",
    response_model=Reporte1Read,
    summary="Actualizar un Reporte 1"
)
def handle_update_reporte1(
    reporte_id: int,
    data: Reporte1Update,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte_existente.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este reporte."
        )
    
    reporte_actualizado = reporte1_service.update_reporte1(
        db=session, reporte_existente=reporte_existente, data=data
    )
    
    return reporte_actualizado


@router.delete(
    "/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un Reporte 1"
)
def handle_delete_reporte1(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte_existente = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte_existente.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este reporte."
        )
    
    reporte1_service.delete_reporte1(db=session, reporte_existente=reporte_existente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{reporte_id}/pdf",
    response_class=StreamingResponse,
    summary="Descargar Reporte 1 en PDF"
)
async def handle_generate_reporte1_pdf(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    reporte = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para generar este reporte."
        )
    
    try:
        pdf_stream: io.BytesIO = pdf_generator_service.generate_reporte1_pdf(
            db=session, reporte_id=reporte_id
        )
        
        proyecto_name = reporte.nombre_proyecto[:20] if len(reporte.nombre_proyecto) > 20 else reporte.nombre_proyecto
        filename = f"Reporte_Avance_{proyecto_name}_{reporte.periodo}.pdf"
        
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