from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import administradores, alumnos, tutores, tutorias, reportes, configuracion  # Importamos el router


app = FastAPI(title="API CRUD Tutorías")

# Configurar CORS
origins = [
    "http://localhost:5173",  # 👈 Vite por defecto
    "http://127.0.0.1:5173",
    # "https://mi-dominio.com"  # 👈 aquí agregas tu dominio real en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # permitir todos los métodos: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # permitir todas las cabeceras
)

# Al iniciar la app, se crean las tablas
@app.on_event("startup")
async def on_startup():
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error during startup: {e}")
        # Optionally, re-raise the exception if it's critical and not a CancelledError
        # However, for graceful reloads, we might just log and continue.
    finally:
        pass # Ensure any cleanup or finalization happens if needed

# Incluir routers
app.include_router(administradores.router, prefix="/api")
app.include_router(alumnos.router, prefix="/api")
app.include_router(tutores.router, prefix="/api")
app.include_router(tutorias.router, prefix="/api")
app.include_router(reportes.router, prefix="/api")
app.include_router(configuracion.router, prefix="/api")
