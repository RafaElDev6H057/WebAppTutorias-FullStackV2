# app/routers/reportes.py

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database import get_session
from app.schemas.reporte_integral import ReporteIntegralCreate, ReporteIntegralRead
from app.services import reporte_integral_service
from app.schemas.reporte1 import Reporte1Create, Reporte1Read
from app.services import reporte1_service
from app.schemas.reporte2 import Reporte2Create, Reporte2Read
from app.services import reporte2_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.post(
    "/integral", 
    response_model=ReporteIntegralRead, 
    status_code=status.HTTP_201_CREATED
)
def handle_create_reporte(
    data: ReporteIntegralCreate,
    session: Session = Depends(get_session)
):
    """
    Endpoint para crear un nuevo reporte integral.
    Siempre crea un nuevo registro y devuelve status 201.
    """
    reporte = reporte_integral_service.create_reporte(db=session, data=data)
    return reporte

@router.post(
    "/general-1",
    response_model=Reporte1Read,
    status_code=status.HTTP_201_CREATED
)
def handle_create_reporte1(
    data: Reporte1Create,
    session: Session = Depends(get_session)
):
    """
    Endpoint para crear un nuevo Reporte General 1.
    """
    reporte1 = reporte1_service.create_reporte1(db=session, data=data)
    return reporte1

@router.post(
    "/general-2",
    response_model=Reporte2Read,
    status_code=status.HTTP_201_CREATED
)
def handle_create_reporte2(
    data: Reporte2Create,
    session: Session = Depends(get_session)
):
    """
    Endpoint para crear un nuevo Reporte General 2.
    """
    reporte2 = reporte2_service.create_reporte2(db=session, data=data)
    return reporte2