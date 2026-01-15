"""
Configuración de base de datos y gestión de sesiones SQLModel.

Soporta entornos híbridos:
- Desarrollo Local: SQLite (sin pooling)
- Producción (Coolify): PostgreSQL con QueuePool optimizado
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from app.core.config import settings

# 1. Definir argumentos de conexión base
connect_args = {}
poolclass = None
engine_kwargs = {}
database_url = settings.DATABASE_URL

# 2. Configuración dinámica según el tipo de base de datos
if "sqlite" in database_url:
    # ============================================================
    # Configuración para SQLite (Desarrollo Local)
    # ============================================================
    # check_same_thread=False es necesario para FastAPI con SQLite
    connect_args = {"check_same_thread": False}

    # SQLite no soporta connection pooling real, usar NullPool
    poolclass = NullPool

    print(f"🗄️  Modo Base de Datos: SQLite (Local)")
    print(f" Ubicación: {database_url}")

elif "postgresql" in database_url:
    # ============================================================
    # Configuración para PostgreSQL (Producción en Coolify)
    # ============================================================
    # QueuePool es el default y el más eficiente para PostgreSQL
    # en servidores dedicados (NO usar NullPool aquí)

    connect_args = {
        "connect_timeout": 10,  # Timeout de conexión inicial
    }

    # Parámetros de pooling optimizados para producción
    engine_kwargs = {
        "pool_size": settings.DB_POOL_SIZE,  # Conexiones permanentes (default: 10)
        "max_overflow": settings.DB_MAX_OVERFLOW,  # Conexiones extra bajo demanda (default: 20)
        "pool_timeout": settings.DB_POOL_TIMEOUT,  # Espera máxima por conexión (default: 30s)
        "pool_recycle": settings.DB_POOL_RECYCLE,  # Reciclar conexiones viejas (default: 1h)
        "pool_pre_ping": True,  # Verificar conexión antes de usarla (CRÍTICO)
    }

    print(f"Modo Base de Datos: PostgreSQL (Producción)")
    print(
        f"Pool Config: size={settings.DB_POOL_SIZE}, overflow={settings.DB_MAX_OVERFLOW}"
    )
    print(f"Pool Recycle: {settings.DB_POOL_RECYCLE}s")

else:
    # Base de datos no soportada
    raise ValueError(f"Base de datos no soportada: {database_url}")

# 3. Construir argumentos del Engine
final_engine_kwargs = {
    "echo": settings.DB_ECHO,  # Logging de SQL (True en dev, False en prod)
    "connect_args": connect_args,
    **engine_kwargs,  # Pool settings (solo para PostgreSQL)
}

# Solo agregar poolclass si está definido (SQLite)
if poolclass:
    final_engine_kwargs["poolclass"] = poolclass

# 4. Crear el Engine
engine = create_engine(database_url, **final_engine_kwargs)


def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.

    ADVERTENCIA DE PRODUCCIÓN:
    Esta función es útil para desarrollo rápido, pero en producción
    es ALTAMENTE RECOMENDADO usar Alembic para migraciones controladas.

    Razones para usar Alembic en producción:
    - Control de versiones de esquema
    - Rollbacks seguros
    - Migraciones progresivas sin pérdida de datos
    - Auditoría de cambios en la BD

    Esta función debe ser llamada al inicio de la aplicación solo en desarrollo.
    """
    if settings.ENV == "production":
        print("ADVERTENCIA: create_db_and_tables() en producción.")

    print("Verificando/Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas listas.")


def get_session():
    """
    Generador de sesiones de base de datos para inyección de dependencias.

    Crea y proporciona una sesión de base de datos que se cierra automáticamente
    al finalizar la petición. Utilizado como dependencia en endpoints de FastAPI.

    Yields:
        Session: Sesión activa de base de datos.

    Ejemplo de uso en FastAPI:
        @app.get("/users/")
        def get_users(session: Session = Depends(get_session)):
            users = session.exec(select(User)).all()
            return users
    """
    with Session(engine) as session:
        yield session
