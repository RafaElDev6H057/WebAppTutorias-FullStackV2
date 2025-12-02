"""
Configuración de base de datos y gestión de sesiones SQLModel.

Adaptado para soportar entorno Híbrido:
- Desarrollo Local: SQLite
- Producción (Render/Supabase): PostgreSQL con NullPool
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from app.core.config import settings

# 1. Definir argumentos de conexión base
connect_args = {}
poolclass = None
database_url = settings.DATABASE_URL

# 2. Configuración dinámica según el tipo de base de datos
if "sqlite" in database_url:
    # Configuración para SQLite (Desarrollo Local)
    # check_same_thread es necesario solo para SQLite en FastAPI
    connect_args = {"check_same_thread": False}
    print(f"🗄️ Modo Base de Datos: SQLite (Local)")

elif "postgresql" in database_url:
    # Configuración para PostgreSQL (Producción / Supabase)
    # NullPool desactiva el pooling de SQLAlchemy, dejando que Supabase
    # (o PgBouncer) gestione las conexiones, evitando errores de "connection closed".
    poolclass = NullPool
    connect_args = {
        "connect_timeout": 15, # Tiempo de espera un poco más holgado
    }
    print(f"🚀 Modo Base de Datos: PostgreSQL (Producción)")

# 3. Crear el Engine
# Usamos argumentos dinámicos (**options) para limpiar el código
engine_options = {
    "echo": settings.DB_ECHO, # Controlado desde .env (True en dev, False en prod)
    "connect_args": connect_args
}

if poolclass:
    engine_options["poolclass"] = poolclass

engine = create_engine(database_url, **engine_options)


def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.
    
    Esta función debe ser llamada al inicio de la aplicación.
    En producción, es recomendable usar Alembic para migraciones,
    pero esto funciona para inicializar estructuras básicas.
    """
    print("📦 Verificando/Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas listas.")


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