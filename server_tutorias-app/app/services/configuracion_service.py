# app/services/configuracion_service.py
from sqlmodel import Session
from app.models.configuracion import ConfiguracionSistema
from app.schemas.configuracion import ConfiguracionUpdate

# El ID de la configuración siempre será 1
CONFIG_ID = 1

def get_configuracion(db: Session) -> ConfiguracionSistema:
    """
    Obtiene la configuración del sistema. Si no existe, la crea.
    """
    config = db.get(ConfiguracionSistema, CONFIG_ID)
    if not config:
        config = ConfiguracionSistema(id=CONFIG_ID, reporte_integral_etapa=1)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

def update_configuracion(db: Session, data: ConfiguracionUpdate) -> ConfiguracionSistema:
    """
    Actualiza la configuración del sistema.
    """
    config = get_configuracion(db) # Obtiene o crea la config
    config.reporte_integral_etapa = data.reporte_integral_etapa
    db.add(config)
    db.commit()
    db.refresh(config)
    return config