"""
Servicio de lógica de negocio para la gestión de Configuración del Sistema.

Proporciona funciones para obtener y actualizar la configuración singleton
que controla las etapas del reporte integral de tutorías.
"""

from sqlmodel import Session

from app.models.configuracion import ConfiguracionSistema
from app.schemas.configuracion import ConfiguracionUpdate

CONFIG_ID = 1


def get_configuracion(db: Session) -> ConfiguracionSistema:
    """
    Obtiene la configuración del sistema.
    
    Si no existe el registro de configuración, lo crea automáticamente
    con valores por defecto (etapa 1).
    
    Args:
        db: Sesión de base de datos.
    
    Returns:
        Instancia de la configuración del sistema.
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
    
    Si no existe el registro de configuración, lo crea antes de actualizarlo.
    
    Args:
        db: Sesión de base de datos.
        data: Datos de actualización con la nueva etapa del reporte.
    
    Returns:
        Instancia de la configuración actualizada.
    """
    config = get_configuracion(db)
    config.reporte_integral_etapa = data.reporte_integral_etapa
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    return config
