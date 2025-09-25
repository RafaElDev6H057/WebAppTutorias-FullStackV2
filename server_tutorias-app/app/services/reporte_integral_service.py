# app/services/reporte_integral_service.py

from sqlmodel import Session
from app.models.reporte_integral import ReporteIntegral
from app.schemas.reporte_integral import ReporteIntegralCreate

def create_reporte(db: Session, data: ReporteIntegralCreate) -> ReporteIntegral:
    """
    Crea un nuevo reporte integral en la base de datos.
    """
    # Simplemente creamos un nuevo reporte con los datos recibidos
    new_report = ReporteIntegral.model_validate(data)
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report