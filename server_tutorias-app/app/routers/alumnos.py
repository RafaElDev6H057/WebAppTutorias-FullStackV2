# app/routers/alumnos.py

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm # Importa el formulario de login
from sqlmodel import Session, select, or_, func
import shutil
import os
from typing import List, Optional
from datetime import timedelta # Importa timedelta para la expiración

# --- Imports de la App ---
from app.database import get_session
from app.models.alumno import Alumno
from app.models.administrador import Administrador # Para proteger rutas de admin
from app.schemas.alumno import (
    AlumnoCreate, AlumnoRead, AlumnoUpdate, AlumnosPage,
    AlumnoSetPassword, AlumnoUpdatePassword
)
from app.schemas.administrador import Token # Importa el esquema del Token
from app.services import alumno_service
from app.core import security # Importa el módulo de seguridad
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES # Importa el tiempo de expiración
# 👇 Importa las dependencias de seguridad de Admin y Alumno
from app.core.dependencies import get_current_admin_user, get_current_alumno_user

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

# =======================================================
# === ENDPOINTS DE AUTENTICACIÓN Y GESTIÓN DE ALUMNOS ===
# =======================================================

# 🔹 Login de alumno (AHORA DEVUELVE TOKEN)
@router.post("/login", response_model=Token, summary="Login para Alumnos")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Usa el formulario OAuth2
    session: Session = Depends(get_session)
):
    # El 'username' del formulario será el num_control
    alumno = alumno_service.get_alumno_by_num_control(session, form_data.username)

    if not alumno:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Número de control o contraseña incorrectos")

    # Lógica de Login Dual (sin cambios)
    is_password_correct = False
    if alumno.requires_password_change:
        is_password_correct = (form_data.password == alumno.contraseña)
    else:
        is_password_correct = security.verify_password(form_data.password, alumno.contraseña)
        
    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Número de control o contraseña incorrectos")
    
    # Creación del Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        # Guardamos el ID del alumno como 'sub' (subject) y el 'role'
        data={"sub": str(alumno.id_alumno), "role": "alumno"}, 
        expires_delta=access_token_expires
    )
    
    # Devuelve el token
    return {"access_token": access_token, "token_type": "bearer"}

# 🔹 Establecer contraseña inicial (SIN TOKEN, LÓGICA ABIERTA)
@router.post("/set-password", summary="Establecer contraseña permanente para Alumno")
def set_password(data: AlumnoSetPassword, session: Session = Depends(get_session)):
    """Permite al alumno usar su contraseña temporal para crear una definitiva."""
    return alumno_service.set_permanent_password(db=session, data=data)

# 🔹 Cambiar contraseña (CON TOKEN DE ALUMNO)
@router.put("/change-password", summary="Cambiar la contraseña de un Alumno autenticado")
def change_password(
    data: AlumnoUpdatePassword,
    # 👇 Protegido por el token del propio alumno
    current_alumno: Alumno = Depends(get_current_alumno_user), 
    session: Session = Depends(get_session)
):
    """Permite al alumno (ya logueado) cambiar su propia contraseña."""
    return alumno_service.change_password(db=session, alumno=current_alumno, data=data)

# ===================================================
# === ENDPOINTS DE GESTIÓN (SOLO PARA ADMINS) ===
# ===================================================

# 🔹 Obtener todos los alumnos (PAGINADO Y PROTEGIDO POR ADMIN)
@router.get("/", response_model=AlumnosPage, summary="Obtener todos los Alumnos (Admin)")
def get_alumnos(
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    search: Optional[str] = Query(None, min_length=3)
):
    """Obtiene una lista paginada de todos los alumnos. (Solo Admins)"""
    query = select(Alumno)
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Alumno.nombre.ilike(search_term),      # type: ignore 
                Alumno.apellido_p.ilike(search_term), # type: ignore
                Alumno.apellido_m.ilike(search_term), # type: ignore
                Alumno.num_control.ilike(search_term) # type: ignore
            )
        )
    count_query = select(func.count()).select_from(query.subquery()) # type: ignore
    total_alumnos = session.exec(count_query).one()
    offset = (page - 1) * size
    alumnos = session.exec(query.offset(offset).limit(size)).all()
    return AlumnosPage(total_alumnos=total_alumnos, alumnos=alumnos) # type: ignore

# 🔹 Cargar Excel de Alumnos (PROTEGIDO POR ADMIN)
@router.post("/upload-excel", summary="Cargar alumnos desde Excel (Admin)")
def upload_alumnos_from_excel(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """Sube un archivo Excel para poblar la base de datos de alumnos. (Solo Admins)"""
    alumnos_cargados = alumno_service.process_and_load_excel(db=session, file=file)
    return {"message": "Alumnos cargados exitosamente.", "alumnos_cargados": alumnos_cargados}

# 🔹 Obtener un alumno por ID (PROTEGIDO POR ADMIN)
@router.get("/{id_alumno}", response_model=AlumnoRead, summary="Obtener un Alumno por ID (Admin)")
def get_alumno(
    id_alumno: int,
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """Obtiene un alumno específico por su ID. (Solo Admins)"""
    alumno = session.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return alumno

# 🔹 Crear un nuevo alumno (PROTEGIDO POR ADMIN)
@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED, summary="Crear un Alumno manualmente (Admin)")
def create_alumno(
    data: AlumnoCreate, 
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """Crea un nuevo alumno manualmente. (Solo Admins)"""
    return alumno_service.create_alumno(db=session, data=data)

# 🔹 Actualizar alumno (PROTEGIDO POR ADMIN)
@router.put("/{id_alumno}", response_model=AlumnoRead, summary="Actualizar un Alumno (Admin)")
def update_alumno(
    id_alumno: int,
    data: AlumnoUpdate, 
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """Actualiza los datos de un alumno existente. (Solo Admins)"""
    alumno = session.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return alumno_service.update_alumno(db=session, alumno=alumno, data=data)

# 🔹 Eliminar alumno (PROTEGIDO POR ADMIN)
@router.delete("/{id_alumno}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Alumno (Admin)")
def delete_alumno(
    id_alumno: int,
    session: Session = Depends(get_session),
    # 👇 Protegido por Admin
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """Elimina un alumno. (Solo Admins)"""
    alumno = session.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    session.delete(alumno)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)