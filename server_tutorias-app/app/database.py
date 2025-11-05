"""
Configuración de base de datos y gestión de sesiones SQLModel.

Configura el motor de base de datos SQLite y proporciona funciones
para inicialización de tablas y generación de sesiones para dependencias.
"""

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.
    
    Esta función debe ser llamada al inicio de la aplicación
    para garantizar que todas las tablas existen en la base de datos.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generador de sesiones de base de datos para inyección de dependencias.
    
    Crea y proporciona una sesión de base de datos que se cierra automáticamente
    al finalizar la petición. Utilizado como dependencia en endpoints de FastAPI.
    
    Yields:
        Session: Sesión activa de base de datos.
    """
    with Session(engine) as session:
        yield session
