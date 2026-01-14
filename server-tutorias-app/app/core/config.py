"""
Configuración central de la aplicación.

Gestiona las variables de entorno para diferentes contextos (Local vs Producción).
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
    
    # --- Base de Datos ---
    # En local usa SQLite por defecto.
    # En Render/Supabase, esta variable DEBE ser provista por el entorno.
    # Nota: Si usas Supabase, asegúrate de que la URL empiece con postgresql:// en vez de postgres://
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    
    # Controla si SQLModel imprime las consultas en consola.
    # Por defecto es True en local para depuración, pero debería ser False en producción.
    DB_ECHO: bool = os.getenv("DB_ECHO", "True").lower() == "true"

    # --- Seguridad ---
    # ¡CRÍTICO! En producción, cambia esto por una cadena larga y aleatoria generada con `openssl rand -hex 32`
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 8 días (ejemplo) o 30 minutos según prefieras

# Instanciamos la clase para que pueda ser importada como 'settings'
settings = Settings()