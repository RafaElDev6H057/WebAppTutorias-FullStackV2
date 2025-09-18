# routers/alumnos.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from typing import List

# ⚙️ Imports refactorizados
from app.database import get_session
from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoRead, AlumnoUpdate, AlumnoLogin
from app.services import alumno_service  # 👈 Importamos nuestro nuevo servicio

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


# ✅ 1. Dependencia reutilizable para obtener el alumno o lanzar 404
def get_alumno_or_404(id_alumno: int, session: Session = Depends(get_session)) -> Alumno:
    alumno = session.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return alumno


# 🔹 Obtener todos los alumnos (sin cambios, ya era simple)
@router.get("/", response_model=List[AlumnoRead])
def get_alumnos(session: Session = Depends(get_session)):
    return session.exec(select(Alumno)).all()


# 🔹 Obtener un alumno por ID
@router.get("/{id_alumno}", response_model=AlumnoRead)
def get_alumno(alumno: Alumno = Depends(get_alumno_or_404)):
    # La lógica de buscar y validar si existe ya está en la dependencia
    return alumno


# 🔹 Crear un nuevo alumno
@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED)
def create_alumno(data: AlumnoCreate, session: Session = Depends(get_session)):
    # Delegamos toda la lógica de creación al servicio
    return alumno_service.create_alumno(db=session, data=data)


# 🔹 Actualizar alumno
@router.put("/{id_alumno}", response_model=AlumnoRead)
def update_alumno(
    data: AlumnoUpdate, 
    alumno: Alumno = Depends(get_alumno_or_404),
    session: Session = Depends(get_session)
):
    # Delegamos la lógica de actualización al servicio
    return alumno_service.update_alumno(db=session, alumno=alumno, data=data)


# 🔹 Eliminar alumno
@router.delete("/{id_alumno}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alumno(alumno: Alumno = Depends(get_alumno_or_404), session: Session = Depends(get_session)):
    # ✅ 2. Respuesta estándar para eliminación exitosa
    session.delete(alumno)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 🔹 Login de alumno
@router.post("/login", response_model=AlumnoRead) # 👈 ¡MUY IMPORTANTE!
def login(data: AlumnoLogin, session: Session = Depends(get_session)):
    alumno = alumno_service.get_alumno_by_num_control(session, data.num_control)

    if not alumno or not alumno_service.verify_password(data.contraseña, alumno.contraseña):
        # ✅ 3. Lanzamos una excepción estándar de "No autorizado"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Número de control o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ✅ 4. ¡NUNCA devuelvas el hash de la contraseña!
    # Usamos AlumnoRead como response_model para filtrar la contraseña automáticamente.
    return alumno