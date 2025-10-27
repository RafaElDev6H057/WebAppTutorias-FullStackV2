# app/routers/tutorias.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Query # 👈 Añadido UploadFile, File
from sqlmodel import Session, select, or_, func
from typing import List, Optional, Union # 👈 Añadido Optional

# Imports de la app
from app.database import get_session
from app.models.tutoria import Tutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate, TutoriaReadWithDetails, TutoriasPage
from app.services import tutoria_service
from app.models.alumno import Alumno
from app.models.tutor import Tutor

# Imports para protección
from app.core.dependencies import get_current_admin_user, get_current_user, get_current_tutor_user, oauth2_scheme_admin, oauth2_scheme_tutor # 👈 Necesario para proteger la nueva ruta
from app.models.administrador import Administrador # Para type hinting

router = APIRouter(prefix="/tutorias", tags=["Tutorias"])


# --- Dependencia reutilizable (ya la teníamos) ---
def get_tutoria_or_404(id_tutoria: int, session: Session = Depends(get_session)) -> Tutoria:
    tutoria = session.get(Tutoria, id_tutoria)
    if not tutoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tutoría no existe.")
    return tutoria

# ==================================
# === ENDPOINTS CRUD (Para Admin) ===
# ==================================
# Nota: Estos endpoints ahora interactúan con tutorías basadas en periodos.
# La lógica original de 'create_tutoria' aún podría tener la restricción de 4 tutorías.

@router.get("/", response_model=List[TutoriaReadWithDetails], summary="Obtener todas las Tutorías (Admin)")
def get_all_tutorias(
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """Obtiene una lista de todos los registros de tutoría."""
    return session.exec(select(Tutoria)).all()

@router.get("/{id_tutoria}", response_model=TutoriaReadWithDetails, summary="Obtener Tutoría por ID (Admin)")
def get_tutoria_by_id(
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """Obtiene los detalles de un registro de tutoría específico."""
    return tutoria

@router.post("/", response_model=TutoriaReadWithDetails, status_code=status.HTTP_201_CREATED, summary="Crear Tutoría Manualmente (Admin)")
def create_tutoria(
    data: TutoriaCreate,
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """Crea un registro de tutoría manualmente."""
    return tutoria_service.create_tutoria(db=session, data=data)

@router.put("/{id_tutoria}", response_model=TutoriaReadWithDetails, summary="Actualizar Tutoría (Admin)")
def update_tutoria(
    data: TutoriaUpdate,
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """Actualiza un registro de tutoría existente."""
    return tutoria_service.update_tutoria(db=session, tutoria=tutoria, data=data)

@router.delete("/{id_tutoria}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Tutoría (Admin)")
def delete_tutoria(
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """Elimina un registro de tutoría."""
    session.delete(tutoria)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# =============================================
# === ENDPOINTS ESPECÍFICOS DE CONSULTA ===
# =============================================

@router.get("/alumno/{id_alumno}", response_model=List[TutoriaReadWithDetails], summary="Obtener Tutorías por Alumno")
def get_tutorias_by_alumno(
    id_alumno: int,
    session: Session = Depends(get_session),
    # Podríamos proteger esto para que solo el admin o el propio alumno/tutor puedan verlo
    # current_user: Union[Administrador, Alumno, Tutor] = Depends(...)
):
    """Obtiene el historial de tutorías de un alumno específico."""
    tutorias = session.exec(select(Tutoria).where(Tutoria.alumno_id == id_alumno)).all()
    return tutorias

# 🔹 Obtener Tutorías por Tutor (PAGINADO, BUSCABLE Y PROTEGIDO)
@router.get("/tutor/{id_tutor}", response_model=TutoriasPage, summary="Obtener Tutorías por Tutor", dependencies=[Depends(oauth2_scheme_admin), Depends(oauth2_scheme_tutor)])
def get_tutorias_by_tutor(
    id_tutor: int,
    session: Session = Depends(get_session),
    current_user: Union[Administrador, Tutor] = Depends(get_current_user),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    search: Optional[str] = Query(None, min_length=3)
):
    # ... (Validación de Permisos - sin cambios) ...
    is_allowed = False
    if isinstance(current_user, Administrador): is_allowed = True
    elif isinstance(current_user, Tutor) and current_user.id_tutor == id_tutor: is_allowed = True
    if not is_allowed: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso.")

    # --- Lógica de Consulta Revisada ---

    # 1. Crear la base de la consulta para OBTENER las tutorías (con JOIN)
    base_query = select(Tutoria).join(Alumno).where(Tutoria.tutor_id == id_tutor)

    # 2. Crear una consulta SEPARADA solo para CONTAR
    count_base_query = select(func.count(Tutoria.id_tutoria)).where(Tutoria.tutor_id == id_tutor) # type: ignore

    # 3. Aplicar el filtro de búsqueda a AMBAS consultas si es necesario
    if search:
        search_term = f"%{search}%"
        search_filter = or_(
            Alumno.nombre.ilike(search_term),      # type: ignore
            Alumno.apellido_p.ilike(search_term), # type: ignore
            Alumno.apellido_m.ilike(search_term), # type: ignore
            Alumno.num_control.ilike(search_term) # type: ignore
        )
        # Aplicar al query principal (que ya tiene el JOIN)
        base_query = base_query.where(search_filter)
        # Aplicar al query de conteo (necesita el JOIN aquí también)
        count_base_query = count_base_query.join(Alumno).where(search_filter) # type: ignore

    # 4. Ejecutar la consulta de conteo
    total_tutorias = session.exec(count_base_query).one()

    # 5. Aplicar paginación y ejecutar la consulta principal
    offset = (page - 1) * size
    tutorias = session.exec(
        base_query.offset(offset).limit(size)
    ).all()

    # 6. Devolver el resultado
    return TutoriasPage(total_tutorias=total_tutorias, tutorias=tutorias) # type: ignore
# ============================================
# === NUEVO ENDPOINT PARA CARGAR CSV ===
# ============================================

@router.post("/upload-assignment", summary="Cargar Asignaciones desde CSV (Admin)", status_code=status.HTTP_200_OK)
def upload_tutoria_assignment(
    file: UploadFile = File(..., description="Archivo CSV con formato específico de asignación"),
    session: Session = Depends(get_session),
    current_admin: Administrador = Depends(get_current_admin_user) # Protegido
):
    """
    Procesa un archivo CSV para crear nuevos registros de tutoría
    asociando alumnos a un tutor para un periodo específico.
    """
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Se requiere un archivo CSV.")

    result = tutoria_service.process_assignment_csv(db=session, file=file)
    return result

# --- FIN DEL ARCHIVO ---