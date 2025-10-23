# app/routers/tutorias.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File # 👈 Añadido UploadFile, File
from sqlmodel import Session, select
from typing import List, Optional # 👈 Añadido Optional

# Imports de la app
from app.database import get_session
from app.models.tutoria import Tutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate, TutoriaReadWithDetails
from app.services import tutoria_service

# Imports para protección
from app.core.dependencies import get_current_admin_user # 👈 Necesario para proteger la nueva ruta
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

@router.get("/tutor/{id_tutor}", response_model=List[TutoriaReadWithDetails], summary="Obtener Tutorías por Tutor")
def get_tutorias_by_tutor(
    id_tutor: int,
    # Podríamos añadir filtro por periodo aquí: periodo: Optional[str] = Query(None)
    session: Session = Depends(get_session),
    # Podríamos proteger esto para que solo el admin o el propio tutor puedan verlo
    # current_user: Union[Administrador, Tutor] = Depends(...)
):
    """Obtiene todos los registros de tutoría asociados a un tutor específico."""
    query = select(Tutoria).where(Tutoria.tutor_id == id_tutor)
    # if periodo:
    #     query = query.where(Tutoria.periodo == periodo)
    tutorias = session.exec(query).all()
    return tutorias

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