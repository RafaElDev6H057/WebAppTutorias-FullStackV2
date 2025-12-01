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
    
    Acepta tanto contraseñas temporales (sin hashear) como permanentes (hasheadas).
    El alumno debe usar su número de control como username.
    """
    alumno = alumno_service.get_alumno_by_num_control(session, form_data.username)
    
    if not alumno:
        raise HTTPException(
            status_code=401,
            detail="Número de control o contraseña incorrectos"
        )
    
    is_password_correct = False
    
    if alumno.requires_password_change:
        is_password_correct = (form_data.password == alumno.contraseña)
    else:
        is_password_correct = security.verify_password(form_data.password, alumno.contraseña)
    
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
    
    return {"access_token": access_token, "token_type": "bearer", "rol": "alumno"}


@router.post("/set-password", summary="Establecer contraseña permanente para Alumno")
def set_password(data: AlumnoSetPassword, session: Session = Depends(get_session)):
    """
    Permite a un alumno establecer su contraseña permanente.
    
    El alumno debe proporcionar su contraseña temporal para validar su identidad
    antes de establecer una nueva contraseña permanente. No requiere autenticación.
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
    
    Requiere proporcionar la contraseña actual para validación.
    Solo disponible para alumnos que ya establecieron su contraseña permanente.
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
    """
    Genera y descarga la constancia de tutorías del alumno autenticado en formato PDF.
    
    El alumno debe haber completado al menos el número mínimo de tutorías requeridas
    para ser elegible. El PDF incluye información del alumno y registro de tutorías.
    
    Returns:
        Stream de bytes del archivo PDF generado.
    
    Raises:
        HTTPException: Si el alumno no es elegible o hay error en la generación.
    """
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
    """
    Obtiene una lista paginada de alumnos con búsqueda opcional.
    
    Accesible para administradores y tutores. Permite buscar por nombre,
    apellidos o número de control.
    
    Args:
        page: Número de página (inicia en 1).
        size: Cantidad de registros por página (máximo 100).
        search: Término de búsqueda opcional (mínimo 3 caracteres).
    
    Returns:
        Página de alumnos con total de registros.
    """
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
    """
    Obtiene el perfil completo del alumno autenticado.
    
    Requiere token de autenticación de alumno.
    
    Returns:
        Datos completos del perfil del alumno.
    """
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
    """
    Obtiene el progreso de tutorías del alumno autenticado.
    
    Retorna el número de tutorías completadas y si el alumno es elegible
    para obtener su constancia de tutorías.
    
    Returns:
        Estado de tutorías con contador y elegibilidad.
    """
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
    """
    Carga masiva de alumnos desde un archivo Excel.
    
    Reemplaza todos los alumnos existentes con los datos del archivo.
    Los alumnos son creados con contraseñas temporales.
    Solo accesible por administradores.
    
    Returns:
        Mensaje de confirmación con número de alumnos cargados.
    """
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
    """
    Obtiene los datos de un alumno específico por su ID.
    
    Solo accesible por administradores.
    
    Raises:
        HTTPException: Si el alumno no existe.
    """
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
    """
    Crea un nuevo alumno manualmente.
    
    El alumno es creado con contraseña permanente (no temporal).
    Solo accesible por administradores.
    
    Returns:
        Datos del alumno creado.
    """
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
    
    Solo accesible por administradores.
    
    Raises:
        HTTPException: Si el alumno no existe.
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
    """
    Elimina un alumno del sistema.
    
    Solo accesible por administradores.
    Esta acción es permanente y no puede deshacerse.
    
    Raises:
        HTTPException: Si el alumno no existe.
    """
    alumno = session.get(Alumno, id_alumno)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    session.delete(alumno)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
