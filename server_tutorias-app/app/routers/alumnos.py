# routers/alumnos.py

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query
from sqlmodel import Session, select, or_, func
import shutil 
import os
from typing import List, Optional

# ⚙️ Imports refactorizados
from app.database import get_session
from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoRead, AlumnoUpdate, AlumnoLogin, AlumnoSetPassword, AlumnoUpdatePassword, AlumnosPage
from app.services import alumno_service  # 👈 Importamos nuestro nuevo servicio

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


# ✅ 1. Dependencia reutilizable para obtener el alumno o lanzar 404
def get_alumno_or_404(id_alumno: int, session: Session = Depends(get_session)) -> Alumno:
    alumno = session.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return alumno


# 🔹 Obtener todos los alumnos (sin cambios, ya era simple)
@router.get("/", response_model=AlumnosPage)
def get_alumnos(
    session: Session = Depends(get_session),
    page: int = Query(1, gt=0, description="Número de página a solicitar"),
    size: int = Query(10, gt=0, le=100, description="Tamaño de la página (máximo 100)"),
    search: Optional[str] = Query(None, min_length=3, description="Término de búsqueda por nombre, apellido o núm. de control")
):
    query = select(Alumno)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Alumno.nombre.ilike(search_term),  #type: ignore 
                Alumno.apellido_p.ilike(search_term), #type: ignore
                Alumno.apellido_m.ilike(search_term), #type: ignore
                Alumno.num_control.ilike(search_term) #type: ignore
            )
        )

    # ✅ 2. Esta consulta ahora funcionará porque 'func' está importado.
    # Usamos .subquery() para que funcione correctamente con la consulta filtrada.
    count_query = select(func.count()).select_from(query.subquery())
    total_alumnos = session.exec(count_query).one()

    offset = (page - 1) * size
    alumnos = session.exec(
        query.offset(offset).limit(size)
    ).all()
    
    return AlumnosPage(total_alumnos=total_alumnos, alumnos=alumnos) #type: ignore


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
@router.post("/login", response_model=AlumnoRead)
def login(data: AlumnoLogin, session: Session = Depends(get_session)):
    alumno = alumno_service.get_alumno_by_num_control(session, data.num_control)

    # Si el alumno no existe, el error es el mismo
    if not alumno:
        raise HTTPException(status_code=401, detail="Número de control o contraseña incorrectos")

    # ✅ LÓGICA DE LOGIN DUAL
    is_password_correct = False
    # Si requiere cambio, es contraseña temporal (comparación directa)
    if alumno.requires_password_change:
        if data.contraseña == alumno.contraseña:
            is_password_correct = True
    # Si no, es contraseña hasheada (verificación)
    else:
        if alumno_service.verify_password(data.contraseña, alumno.contraseña):
            is_password_correct = True
            
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Número de control o contraseña incorrectos")

    return alumno

@router.post("/set-password", summary="Establecer contraseña permanente para un alumno")
def set_password(data: AlumnoSetPassword, session: Session = Depends(get_session)):
    """
    Permite a un alumno con contraseña temporal establecer su
    contraseña final y segura.
    """
    return alumno_service.set_permanent_password(db=session, data=data)

@router.put("/{id_alumno}/change-password", summary="Cambiar la contraseña de un alumno existente")
def update_password(
    data: AlumnoUpdatePassword,
    alumno: Alumno = Depends(get_alumno_or_404), # Reutilizamos nuestra dependencia
    session: Session = Depends(get_session)
):
    """
    Permite a un alumno ya registrado (con contraseña hasheada) 
    cambiar su contraseña.
    """
    return alumno_service.change_password(db=session, alumno=alumno, data=data)

@router.post("/upload-excel", summary="Cargar alumnos desde un archivo Excel")
def upload_alumnos_from_excel(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """
    Sube un archivo Excel para poblar la base de datos de alumnos.
    La operación es rápida y la respuesta es inmediata.
    
    **Importante**: Esta operación BORRA todos los alumnos y tutorías existentes
    y los reemplaza con los datos del archivo.
    """
    # ✅ Llamada directa a la función del servicio
    alumnos_cargados = alumno_service.process_and_load_excel(db=session, file=file)
    
    return {
        "message": "Archivo procesado y alumnos cargados exitosamente.",
        "alumnos_cargados": alumnos_cargados
    }