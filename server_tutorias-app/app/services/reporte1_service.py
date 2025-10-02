from sqlmodel import Session
from app.models.reporte1 import Reporte1
from app.schemas.reporte1 import Reporte1Create

def create_reporte1(db: Session, data: Reporte1Create) -> Reporte1:
    """
    Crea un nuevo Reporte General 1 en la base de datos.
    """
    # Creamos una instancia del modelo Reporte1 a partir de los datos del schema
    new_reporte1 = Reporte1.model_validate(data)
    
    # Añadimos, confirmamos y refrescamos la sesión para obtener el objeto completo
    db.add(new_reporte1)
    db.commit()
    db.refresh(new_reporte1)
    
    return new_reporte1