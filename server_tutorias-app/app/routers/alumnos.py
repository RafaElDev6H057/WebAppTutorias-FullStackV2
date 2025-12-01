"""
Endpoints de la API para gestión de Alumnos.

Proporciona endpoints para autenticación, operaciones CRUD, gestión de contraseñas,
carga masiva desde Excel y generación de constancias de tutorías.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select, or_, func
from typing import Optional, Union
from datetime import timedelta
import io

from app.database import get_session
from app.models.alumno import Alumno
from app.models.administrador import Administrador
from app.models.tutor import Tutor
from app.schemas.alumno import (
    AlumnoCreate,
    AlumnoRead,
    AlumnoUpdate,
    AlumnosPage,
    AlumnoSetPassword,
    AlumnoUpdatePassword,
    AlumnoTutoriaStatus
)
from app.schemas.administrador import Token
from app.services import alumno_service
from app.services import pdf_generator_service
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import (
    get_current_admin_user,
    get_current_alumno_user,
    get_current_user,
    oauth2_scheme_admin,
    oauth2_scheme_tutor
)

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.post("/login", response_model=Token, summary="Login para Alumnos")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Autentica a un alumno y genera un token JWT.
    
    Soporta Login Híbrido:
    1. Intenta validar contraseña como Hash (seguro).
    2. Si falla y el alumno requiere cambio, intenta validar como texto plano (temporal).
    """
    alumno = alumno_service.get_alumno_by_num_control(session, form_data.username)
    
    if not alumno:
        raise HTTPException(
            status_code=401,
            detail="Número de control o contraseña incorrectos"
        )
    
    is_password_correct = False
    
    # --- VALIDACIÓN ROBUSTA ---
    
    # 1. Intento Prioritario: Verificar Hash (Lo estándar y seguro)
    # Esto cubre: Alumnos activos y Alumnos cuya contraseña reseteó el Admin
    try:
        if security.verify_password(form_data.password, alumno.contraseña):
            is_password_correct = True
    except Exception:
        # verify_password puede fallar si la BD tiene texto plano que no parece hash (caso Excel)
        pass 
        
    # 2. Intento Secundario: Texto Plano (Solo si tiene la bandera activa)
    # Esto cubre: Alumnos recién importados de Excel
    if not is_password_correct and alumno.requires_password_change:
        if form_data.password == alumno.contraseña:
            is_password_correct = True
    
    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Número de control o contraseña incorrectos"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(alumno.id_alumno), "role": "alumno"},
        expires_delta=access_token_expires
    )
    
    # Devolvemos el rol explícito 'alumno'
    return {"access_token": access_token, "token_type": "bearer", "rol": "alumno"}


@router.post("/set-password", summary="Establecer contraseña permanente para Alumno")
def set_password(data: AlumnoSetPassword, session: Session = Depends(get_session)):
    """
    Permite a un alumno establecer su contraseña permanente.
    """
    return alumno_service.set_permanent_password(db=session, data=data)


@router.put("/change-password", summary="Cambiar la contraseña de un Alumno autenticado")
def change_password(
    data: AlumnoUpdatePassword,
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    """
    Permite a un alumno autenticado cambiar su contraseña permanente.
    """
    return alumno_service.change_password(db=session, alumno=current_alumno, data=data)


@router.get(
    "/me/constancia-pdf",
    summary="Descargar Constancia de Tutorías",
    response_class=StreamingResponse
)
async def handle_generate_constancia_pdf(
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    try:
        pdf_stream: io.BytesIO = pdf_generator_service.generate_constancia_pdf(
            db=session,
            id_alumno=current_alumno.id_alumno # type: ignore
        )
        
        filename = f"Constancia_Tutorias_{current_alumno.num_control}.pdf"
        
        return StreamingResponse(
            content=pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al generar la constancia."
        )


@router.get(
    "/",
    response_model=AlumnosPage,
    summary="Obtener todos los Alumnos (Admin o Tutor)",
    dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)]
)
def get_alumnos(
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    search: Optional[str] = Query(None, min_length=3)
):
    query = select(Alumno)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_( 
                Alumno.nombre.ilike(search_term), # type: ignore
                Alumno.apellido_p.ilike(search_term), # type: ignore
                Alumno.apellido_m.ilike(search_term), # type: ignore
                Alumno.num_control.ilike(search_term) # type: ignore
            )
        )
    
    count_query = select(func.count()).select_from(query.subquery())
    total_alumnos = session.exec(count_query).one()
    
    offset = (page - 1) * size
    alumnos = session.exec(query.offset(offset).limit(size)).all()
    
    return AlumnosPage(total_alumnos=total_alumnos, alumnos=alumnos) # type: ignore


@router.get("/me", response_model=AlumnoRead, summary="Obtener datos del Alumno autenticado")
def read_current_alumno(current_alumno: Alumno = Depends(get_current_alumno_user)):
    return current_alumno


@router.get(
    "/me/estado-tutorias",
    response_model=AlumnoTutoriaStatus,
    summary="Obtener estado de tutorías del Alumno"
)
def get_tutoria_status(
    current_alumno: Alumno = Depends(get_current_alumno_user),
    session: Session = Depends(get_session)
):
    return alumno_service.get_alumno_tutoria_status(
        db=session,
        id_alumno=current_alumno.id_alumno # type: ignore
    )


@router.post("/upload-excel", summary="Cargar alumnos desde Excel (Admin)")
def upload_alumnos_from_excel(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumnos_cargados = alumno_service.process_and_load_excel(db=session, file=file)
    
    return {
        "message": "Alumnos cargados exitosamente.",
        "alumnos_cargados": alumnos_cargados
    }


@router.get("/{id_alumno}", response_model=AlumnoRead, summary="Obtener un Alumno por ID (Admin)")
def get_alumno(
    id_alumno: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumno = session.get(Alumno, id_alumno)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return alumno


@router.post(
    "/",
    response_model=AlumnoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un Alumno manualmente (Admin)"
)
def create_alumno(
    data: AlumnoCreate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    return alumno_service.create_alumno(db=session, data=data)


@router.put("/{id_alumno}", response_model=AlumnoRead, summary="Actualizar un Alumno (Admin)")
def update_alumno(
    id_alumno: int,
    data: AlumnoUpdate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    """
    Actualiza los datos de un alumno existente.
    
    Si el Admin proporciona una nueva contraseña, esta será hasheada
    y el alumno podrá loguearse con ella inmediatamente.
    """
    alumno = session.get(Alumno, id_alumno)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return alumno_service.update_alumno(db=session, alumno=alumno, data=data)


@router.delete("/{id_alumno}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un Alumno (Admin)")
def delete_alumno(
    id_alumno: int,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user)
):
    alumno = session.get(Alumno, id_alumno)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    session.delete(alumno)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)