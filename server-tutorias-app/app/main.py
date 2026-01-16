"""
Punto de entrada principal de la aplicación FastAPI.

Configura la aplicación, middlewares CORS, inicialización de base de datos
y registro de todos los routers del sistema de gestión de tutorías.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import create_db_and_tables, engine
from app.routers import (
    administradores,
    alumnos,
    avisos,
    tutores,
    tutorias,
    configuracion,
    canalizaciones,
    reportes_integral,
    reportes_general1,
    reportes_general2,
    reportes_anexos
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    Crea las tablas al iniciar si no existen.
    """
    try:
        create_db_and_tables()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error durante inicialización: {e}")
    yield


app = FastAPI(
    title="API CRUD Tutorías",
    version="1.0.0",
    lifespan=lifespan
)


# --- CONFIGURACIÓN DE CORS ---
# CORS_ORIGINS ya viene como lista desde settings.CORS_ORIGINS
origins = [origin.strip() for origin in settings.CORS_ORIGINS]

print(f"🌐 CORS configurado para: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registro de Routers
app.include_router(administradores.router, prefix="/api")
app.include_router(alumnos.router, prefix="/api")
app.include_router(tutores.router, prefix="/api")
app.include_router(tutorias.router, prefix="/api")
app.include_router(avisos.router, prefix="/api")
app.include_router(configuracion.router, prefix="/api")
app.include_router(canalizaciones.router, prefix="/api")
app.include_router(reportes_integral.router, prefix="/api")
app.include_router(reportes_general1.router, prefix="/api")
app.include_router(reportes_general2.router, prefix="/api")
app.include_router(reportes_anexos.router, prefix="/api")


@app.get("/")
def read_root():
    """Endpoint raíz de la API"""
    return {
        "message": "API de Tutorías operando correctamente",
        "version": "1.0.0",
        "environment": settings.ENV
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint para Docker/Coolify.
    Verifica el estado de la API y la conexión a la base de datos.
    """
    try:
        # Intenta hacer una query simple para verificar la conexión a la DB
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    return {
        "status": "healthy",
        "service": "tutorias-backend",
        "database": db_status,
        "environment": settings.ENV
    }
