from sqlmodel import Session
from app.models.reporte2 import Reporte2
from app.schemas.reporte2 import Reporte2Create

def create_reporte2(db: Session, data: Reporte2Create) -> Reporte2:
    """
    Crea un nuevo Reporte General 2 en la base de datos.
    """
    # Creamos la instancia del modelo a partir de los datos validados del schema
    new_reporte2 = Reporte2.model_validate(data)
    
    # Guardamos el nuevo reporte en la base de datos
    db.add(new_reporte2)
    db.commit()
    db.refresh(new_reporte2)
    
    return new_reporte2