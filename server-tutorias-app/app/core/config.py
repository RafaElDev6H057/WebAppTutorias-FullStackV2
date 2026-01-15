"""
Configuración central de la aplicación.

Gestiona las variables de entorno para diferentes contextos (Desarrollo vs Producción).
Utiliza una clase 'Settings' para agrupar la configuración y permitir
acceso tipado en el resto de la aplicación.
"""

import os
from dotenv import load_dotenv

# Carga variables desde el archivo .env si existe (solo desarrollo local)
load_dotenv()


class Settings:
    # --- Configuración General ---
    PROJECT_NAME: str = "Sistema de Gestión de Tutorías"
    API_V1_STR: str = "/api"

    # --- Entorno ---
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # --- Base de Datos ---
    # En local usa SQLite por defecto.
    # En producción (Coolify), esta variable DEBE ser provista por el entorno.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

    # Controla si SQLModel imprime las consultas en consola.
    # True en desarrollo para depuración, False en producción.
    DB_ECHO: bool = os.getenv("DB_ECHO", "True").lower() == "true"

    # --- Connection Pool Settings (PostgreSQL) ---
    # Número de conexiones permanentes en el pool
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))

    # Conexiones adicionales permitidas cuando el pool está lleno
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))

    # Reciclar conexiones después de N segundos (evita conexiones obsoletas)
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # 1 hora

    # Timeout para obtener una conexión del pool (segundos)
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # --- Seguridad ---
    # ¡CRÍTICO! En producción, cambia esto por una cadena larga y aleatoria
    # Genera con: openssl rand -hex 32
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480")
    )  # 8 horas

    # --- CORS ---
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

    @staticmethod
    def normalize_database_url(url: str) -> str:
        """
        Normaliza la URL de la base de datos.

        Algunas plataformas legacy usan 'postgres://' en vez de 'postgresql://'
        que no es compatible con SQLAlchemy 1.4+

        Args:
            url: URL de conexión a la base de datos

        Returns:
            URL normalizada
        """
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url


# Instanciamos la clase para que pueda ser importada como 'settings'
settings = Settings()

# Normalizar DATABASE_URL al instanciar
settings.DATABASE_URL = Settings.normalize_database_url(settings.DATABASE_URL)
