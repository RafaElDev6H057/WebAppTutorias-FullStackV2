"""
Punto de entrada principal de la aplicación FastAPI.

Configura la aplicación, middlewares CORS, inicialización de base de datos
y registro de todos los routers del sistema de gestión de tutorías.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
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
    except Exception as e:
        print(f"Error durante inicialización: {e}")
    yield

app = FastAPI(
    title="API CRUD Tutorías",
    version="1.0.0",
    lifespan=lifespan
)

# --- CONFIGURACIÓN DE CORS ---
origins = [
    # Desarrollo Local
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    
    # Producción (Vercel)
    "https://web-app-tutorias.vercel.app", 
]

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
    return {"message": "API de Tutorías operando correctamente."}