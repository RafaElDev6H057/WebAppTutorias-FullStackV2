# app/routers/alumnos.py

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query
from fastapi.responses import StreamingResponse
import io
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select, or_, func
import shutil
import os
from typing import List, Optional
from datetime import timedelta

# --- Imports de la App ---
from app.database import get_session
from app.models.alumno import Alumno
from app.models.administrador import Administrador
from app.schemas.alumno import (
    AlumnoCreate, AlumnoRead, AlumnoUpdate, AlumnosPage,
    AlumnoSetPassword, AlumnoUpdatePassword, AlumnoTutoriaStatus # 👈 Importamos el nuevo schema
)
from app.schemas.administrador import Token
from app.services import alumno_service
from app.services import pdf_generator_service
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_current_admin_user, get_current_alumno_user

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

# =======================================================
# === ENDPOINTS DE AUTENTICACIÓN Y GESTIÓN DE ALUMNOS ===
# =======================================================

# 🔹 Login de alumno
@router.post("/login", response_model=Token, summary="Login para Alumnos")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # ... (código de login sin cambios) ...
    alumno = alumno_service.get_alumno_by_num_control(session, form_data.username)
    if not alumno:
        raise HTTPException(status_code=401, detail="Número de control o contraseña incorrectos")
    is_password_correct = False
    if alumno.requires_password_change:
        is_password_correct = (form_data.password == alumno.contraseña)
    else:
        is_password_correct = security.verify_password(form_data.password, alumno.contraseña)
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Número de control o contraseña incorrectos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(alumno.id_alumno), "role": "alumno"}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 🔹 Establecer contraseña inicial (SIN TOKEN)
@router.post("/set-password", summary="Establecer contraseña permanente para Alumno")
def set_password(data: AlumnoSetPassword, session: Session = Depends(get_session)):
    """Permite al alumno usar su contraseña temporal para crear una definitiva."""
    return alumno_service.set_permanent_password(db=session, data=data)

# 🔹 Cambiar contraseña (CON TOKEN DE ALUMNO)
@router.put("/change-password", summary="Cambiar la contraseña de un Alumno autenticado")
def change_password(
    data: AlumnoUpdatePassword,
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    """Permite al alumno (ya logueado) cambiar su propia contraseña."""
    return alumno_service.change_password(db=session, alumno=current_alumno, data=data)

@router.get(
    "/me/constancia-pdf",
    summary="Descargar Constancia de Tutorías",
    response_class=StreamingResponse # Indicamos que la respuesta es un stream
)
async def handle_generate_constancia_pdf(
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    """
    Genera y devuelve el PDF de la constancia de tutorías
    para el alumno autenticado.
    Falla si el alumno no ha completado las 4 tutorías.
    """
    try:
        # 1. Llamar al servicio de generación de PDF
        pdf_stream: io.BytesIO = pdf_generator_service.generate_constancia_pdf(
            db=session, id_alumno=current_alumno.id_alumno #type: ignore
        )
        
        # 2. Definir el nombre del archivo
        filename = f"Constancia_Tutorias_{current_alumno.num_control}.pdf"

        # 3. Devolver el stream como una respuesta PDF que fuerza la descarga
        return StreamingResponse(
            content=pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException as http_exc:
        # Re-lanzar errores conocidos (ej. 400 si no es elegible)
        raise http_exc
    except Exception as e:
        # Capturar errores inesperados del generador de PDF
        print(f"ERROR INESPERADO al generar constancia PDF para alumno {current_alumno.id_alumno}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al generar la constancia."
        )

# ===================================================
# === ENDPOINTS PROPIOS DEL ALUMNO (PANEL ALUMNO) ===
# ===================================================

@router.get("/me", response_model=AlumnoRead, summary="Obtener datos del Alumno autenticado")
def read_current_alumno(
    current_alumno: Alumno = Depends(get_current_alumno_user)
):
    """
    Obtiene el perfil del alumno actualmente logueado.
    Requiere un token de Alumno.
    """
    # La dependencia get_current_alumno_user ya hace todo el trabajo
    return current_alumno

@router.get("/me/estado-tutorias", response_model=AlumnoTutoriaStatus, summary="Obtener estado de tutorías del Alumno")
def get_tutoria_status(
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    """
    Verifica el progreso de tutorías del alumno (cuántas ha completado)
    para determinar si es elegible para su constancia.
    Requiere un token de Alumno.
    """
    return alumno_service.get_alumno_tutoria_status(db=session, id_alumno=current_alumno.id_alumno) #type: ignore

# ===================================================
# === ENDPOINTS DE GESTIÓN (SOLO PARA ADMINS) ===
# ===================================================

# 🔹 Obtener todos los alumnos (PAGINADO Y PROTEGIDO POR ADMIN)
@router.get("/", response_model=AlumnosPage, summary="Obtener todos los Alumnos (Admin)")
def get_alumnos(
    # ... (código sin cambios) ...
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    search: Optional[str] = Query(None, min_length=3)
):
    # ... (código sin cambios) ...
    query = select(Alumno)
    if search:
        search_term = f"%{search}%"
        query = query.where(or_(Alumno.nombre.ilike(search_term), Alumno.apellido_p.ilike(search_term), Alumno.apellido_m.ilike(search_term), Alumno.num_control.ilike(search_term))) # type: ignore
    count_query = select(func.count()).select_from(query.subquery()) # type: ignore
    total_alumnos = session.exec(count_query).one()
    offset = (page - 1) * size
    alumnos = session.exec(query.offset(offset).limit(size)).all()
    return AlumnosPage(total_alumnos=total_alumnos, alumnos=alumnos) # type: ignore

# 🔹 Cargar Excel de Alumnos (PROTEGIDO POR ADMIN)
@router.post("/upload-excel", summary="Cargar alumnos desde Excel (Admin)")
def upload_alumnos_from_excel(
    # ... (código sin cambios) ...
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumnos_cargados = alumno_service.process_and_load_excel(db=session, file=file)
    return {"message": "Alumnos cargados exitosamente.", "alumnos_cargados": alumnos_cargados}

# 🔹 Obtener un alumno por ID (PROTEGIDO POR ADMIN)
@router.get("/{id_alumno}", response_model=AlumnoRead, summary="Obtener un Alumno por ID (Admin)")
def get_alumno(
    # ... (código sin cambios) ...
    id_alumno: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumno = session.get(Alumno, id_alumno)
    if not alumno: raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return alumno

# 🔹 Crear un nuevo alumno (PROTEGIDO POR ADMIN)
@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED, summary="Crear un Alumno manualmente (Admin)")
def create_alumno(
    # ... (código sin cambios) ...
    data: AlumnoCreate, 
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    return alumno_service.create_alumno(db=session, data=data)

# 🔹 Actualizar alumno (PROTEGIDO POR ADMIN)
@router.put("/{id_alumno}", response_model=AlumnoRead, summary="Actualizar un Alumno (Admin)")
def update_alumno(
    # ... (código sin cambios) ...
    id_alumno: int,
    data: AlumnoUpdate, 
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumno = session.get(Alumno, id_alumno)
    if not alumno: raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return alumno_service.update_alumno(db=session, alumno=alumno, data=data)

# 🔹 Eliminar alumno (PROTEGIDO POR ADMIN)
@router.delete("/{id_alumno}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Alumno (Admin)")
def delete_alumno(
    # ... (código sin cambios) ...
    id_alumno: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumno = session.get(Alumno, id_alumno)
    if not alumno: raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    session.delete(alumno)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)