"""
Punto de entrada principal de la aplicación FastAPI.

Configura la aplicación, middlewares CORS, inicialización de base de datos
y registro de todos los routers del sistema de gestión de tutorías.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import (
    administradores,
    alumnos,
    avisos,
    tutores,
    tutorias,
    reportes,
    configuracion,
    canalizaciones
)

app = FastAPI(title="API CRUD Tutorías")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """
    Evento de inicio de la aplicación.
    
    Crea las tablas de la base de datos si no existen.
    Maneja errores de inicialización de forma silenciosa para
    permitir recargas graciosas durante el desarrollo.
    """
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error durante inicialización: {e}")


app.include_router(administradores.router, prefix="/api")
app.include_router(alumnos.router, prefix="/api")
app.include_router(tutores.router, prefix="/api")
app.include_router(tutorias.router, prefix="/api")
app.include_router(reportes.router, prefix="/api")
app.include_router(avisos.router, prefix="/api")
app.include_router(configuracion.router, prefix="/api")
app.include_router(canalizaciones.router, prefix="/api")
