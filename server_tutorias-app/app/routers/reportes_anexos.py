from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
import io

from app.database import get_session
from app.services import excel_generator_service
from app.core.dependencies import get_current_admin_user
from app.models.administrador import Administrador

router = APIRouter(prefix="/reportes/anexo-3", tags=["Reportes Anexos"])


@router.get(
    "/excel/{periodo}",
    summary="Generar Excel del Anexo 3 por Periodo (Admin)",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}
        }
    },
    response_class=StreamingResponse
)
async def handle_generate_anexo3_excel(
    periodo: str,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Genera y devuelve el archivo Excel "Anexo 3" (Hoja 1 y 2).
    """
    try:
        excel_stream: io.BytesIO = excel_generator_service.generate_anexo3_reporte(
            db=session, periodo=periodo
        )

        filename = f"ANEXO_3_Periodo_{periodo}.xlsx"

        return StreamingResponse(
            content=excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"ERROR INESPERADO al generar Excel Anexo 3 para {periodo}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al generar el reporte Excel."
        )