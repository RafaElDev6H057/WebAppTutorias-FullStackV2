"""
Endpoints de la API para gestión de Reportes.

Proporciona endpoints CRUD para reportes integrales de tutorías, reportes
generales de proyectos (Reporte1) y otros reportes del sistema, con control
de acceso dual (administradores y tutores) y generación de PDFs.
"""

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import List, Union
import io

from app.database import get_session
from app.models.reporte_integral import ReporteIntegral
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralRead, ReporteIntegralUpdate
from app.services import reporte_integral_service, excel_generator_service
from app.services import pdf_generator_service
from app.core.dependencies import get_current_user, get_current_tutor_user, oauth2_scheme_tutor, get_current_admin_user
from app.models.administrador import Administrador
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria

from app.models.reporte1 import Reporte1
from app.schemas.reporte1 import Reporte1Create, Reporte1Read, Reporte1Update
from app.services import reporte1_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.post(
    "/integral",
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
    
    Si no existe un reporte para la tutoría especificada, lo crea.
    Si ya existe, actualiza sus campos con los valores proporcionados.
    Actualiza la bandera reporte_integral_guardado en la tutoría.
    
    Los tutores solo pueden crear/actualizar reportes de sus propias tutorías.
    Los administradores pueden gestionar cualquier reporte.
    
    Raises:
        HTTPException: Si un tutor intenta modificar un reporte de otra tutoría.
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
    "/integral/tutoria/{id_tutoria}",
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
    
    Los tutores solo pueden consultar reportes de sus propias tutorías.
    Los administradores pueden consultar cualquier reporte.
    
    Returns:
        Reporte integral de la tutoría.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
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
    "/integral/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Obtener Reporte Integral por ID"
)
def handle_get_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene un reporte integral específico por su ID.
    
    Los tutores solo pueden consultar reportes de sus propias tutorías.
    Los administradores pueden consultar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
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
    "/integral/{reporte_id}",
    response_model=ReporteIntegralRead,
    summary="Actualizar Reporte Integral"
)
def handle_update_reporte(
    reporte_id: int,
    data: ReporteIntegralUpdate,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Actualiza un reporte integral existente.
    
    Los tutores solo pueden actualizar reportes de sus propias tutorías.
    Los administradores pueden actualizar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
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
    "/integral/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Reporte Integral"
)
def handle_delete_reporte(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Elimina un reporte integral existente.
    
    Actualiza automáticamente la bandera reporte_integral_guardado de la tutoría.
    Los tutores solo pueden eliminar reportes de sus propias tutorías.
    Los administradores pueden eliminar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
    reporte_existente = reporte_integral_service.get_reporte(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor):
        tutoria_asociada = session.get(Tutoria, reporte_existente.id_tutoria) #type: ignore
        
        if not tutoria_asociada or tutoria_asociada.tutor_id != current_user.id_tutor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso."
            )
    
    reporte_integral_service.delete_reporte(db=session, reporte_id=reporte_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/integral/pdf/tutor/{id_tutor}/periodo/{periodo}",
    summary="Generar PDF del Reporte Integral por Tutor y Periodo",
    response_class=StreamingResponse
)
async def handle_generate_integral_pdf(
    id_tutor: int,
    periodo: str,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Genera y descarga un PDF consolidado del reporte integral.
    
    El PDF incluye todos los reportes integrales de los alumnos
    asignados a un tutor específico en un periodo determinado.
    
    Los tutores solo pueden generar PDFs de sus propios reportes.
    Los administradores pueden generar PDFs de cualquier tutor.
    
    Returns:
        Stream del archivo PDF generado.
    
    Raises:
        HTTPException: Si el tutor no tiene permisos o hay error en la generación.
    """
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


@router.post(
    "/general-1",
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
    """
    Crea un nuevo Reporte General 1 (reporte de proyecto de tutor).
    
    Solo accesible por tutores autenticados. El reporte se asocia
    automáticamente al tutor que lo crea.
    
    Returns:
        Datos del reporte creado.
    """
    reporte1 = reporte1_service.create_reporte1(db=session, data=data, tutor_id=current_tutor.id_tutor) #type: ignore
    return reporte1


@router.get(
    "/general-1/tutor",
    response_model=List[Reporte1Read],
    summary="Obtener todos los Reportes 1 del Tutor autenticado",
    dependencies=[Depends(oauth2_scheme_tutor)]
)
def handle_get_reportes1_por_tutor(
    session: Session = Depends(get_session),
    current_tutor: Tutor = Depends(get_current_tutor_user)
):
    """
    Obtiene todos los Reportes Generales 1 creados por el tutor autenticado.
    
    Solo accesible por tutores. Retorna todos los reportes del tutor
    ordenados del más reciente al más antiguo.
    
    Returns:
        Lista de reportes del tutor.
    """
    reportes = reporte1_service.get_reportes_por_tutor(db=session, tutor_id=current_tutor.id_tutor) #type: ignore
    return reportes


@router.get(
    "/general-1/{reporte_id}",
    response_model=Reporte1Read,
    summary="Obtener un Reporte 1 específico por ID"
)
def handle_get_reporte1_por_id(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Obtiene un Reporte General 1 específico por su ID.
    
    Los tutores solo pueden consultar sus propios reportes.
    Los administradores pueden consultar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
    reporte = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este reporte."
        )
    
    return reporte


@router.put(
    "/general-1/{reporte_id}",
    response_model=Reporte1Read,
    summary="Actualizar un Reporte 1"
)
def handle_update_reporte1(
    reporte_id: int,
    data: Reporte1Update,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Actualiza un Reporte General 1 existente.
    
    Los tutores solo pueden actualizar sus propios reportes.
    Los administradores pueden actualizar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
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
    "/general-1/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un Reporte 1"
)
def handle_delete_reporte1(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Elimina un Reporte General 1 existente.
    
    Los tutores solo pueden eliminar sus propios reportes.
    Los administradores pueden eliminar cualquier reporte.
    
    Raises:
        HTTPException: Si el reporte no existe o el tutor no tiene permisos.
    """
    reporte_existente = reporte1_service.get_reporte1_por_id(db=session, reporte_id=reporte_id)
    
    if isinstance(current_user, Tutor) and reporte_existente.id_tutor != current_user.id_tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este reporte."
        )
    
    reporte1_service.delete_reporte1(db=session, reporte_existente=reporte_existente)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/general-1/{reporte_id}/pdf",
    response_class=StreamingResponse,
    summary="Descargar Reporte 1 en PDF"
)
async def handle_generate_reporte1_pdf(
    reporte_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user)
):
    """
    Genera y descarga el PDF del Reporte 1 (Avance de Proyecto).
    
    El PDF incluye todos los detalles del proyecto: objetivos, metas,
    actividades, avance y conclusiones.
    
    Los tutores solo pueden generar PDFs de sus propios reportes.
    Los administradores pueden generar PDFs de cualquier reporte.
    
    Returns:
        Stream del archivo PDF generado.
    
    Raises:
        HTTPException: Si el reporte no existe, el tutor no tiene permisos
                    o hay error en la generación.
    """
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
    
# ==================================
# === GENERACIÓN DE EXCEL ANEXO 3 ===
# ==================================

@router.get(
    "/anexo-3/excel/{periodo}",
    summary="Generar Excel del Anexo 3 por Periodo (Admin)",
    # Definimos el tipo de respuesta para que Swagger sepa qué esperar
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}
        }
    },
    response_class=StreamingResponse # La respuesta real es un stream
)
async def handle_generate_anexo3_excel(
    periodo: str,
    session: Session = Depends(get_session),
    # Protegido: Solo Admins
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Genera y devuelve el archivo Excel "Anexo 3" (Hoja 1 y 2)
    parcialmente rellenado con los datos de la BD para un periodo específico.
    """
    try:
        # 1. Llamar al servicio que genera el Excel en memoria (BytesIO)
        excel_stream: io.BytesIO = excel_generator_service.generate_anexo3_reporte(
            db=session, periodo=periodo
        )

        # 2. Definir el nombre del archivo
        filename = f"ANEXO_3_Periodo_{periodo}.xlsx"

        # 3. Devolver el stream como una respuesta Excel
        return StreamingResponse(
            content=excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException as http_exc:
        # Re-lanzar errores conocidos (ej. 404 si no hay tutorías)
        raise http_exc
    except Exception as e:
        print(f"ERROR INESPERADO al generar Excel Anexo 3 para {periodo}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al generar el reporte Excel."
        )


# ==================================================================================
# === ENDPOINTS DE REPORTE2 - COMENTADOS TEMPORALMENTE
# ==================================================================================
# TODO: Refactorizar cuando se proporcionen models/reporte2.py y schemas/reporte2.py
