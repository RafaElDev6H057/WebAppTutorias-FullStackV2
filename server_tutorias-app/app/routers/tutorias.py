# app/routers/tutorias.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.tutoria import Tutoria
# ✨ ¡Usamos el esquema mejorado para las respuestas!
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate, TutoriaReadWithDetails
from app.services import tutoria_service

router = APIRouter(prefix="/tutorias", tags=["Tutorias"])


# ✅ Dependencia reutilizable para obtener la tutoría o 404
def get_tutoria_or_404(id_tutoria: int, session: Session = Depends(get_session)) -> Tutoria:
    tutoria = session.get(Tutoria, id_tutoria)
    if not tutoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tutoría no existe.")
    return tutoria


# 🔹 Obtener todas las tutorías
@router.get("/", response_model=List[TutoriaReadWithDetails])
def get_all_tutorias(session: Session = Depends(get_session)):
    return session.exec(select(Tutoria)).all()


# 🔹 Obtener una tutoría por su ID
@router.get("/{id_tutoria}", response_model=TutoriaReadWithDetails)
def get_tutoria_by_id(tutoria: Tutoria = Depends(get_tutoria_or_404)):
    return tutoria


# 🔹 Crear nueva tutoría
@router.post("/", response_model=TutoriaReadWithDetails, status_code=status.HTTP_201_CREATED)
def create_tutoria(data: TutoriaCreate, session: Session = Depends(get_session)):
    return tutoria_service.create_tutoria(db=session, data=data)


# 🔹 Actualizar tutoría
@router.put("/{id_tutoria}", response_model=TutoriaReadWithDetails)
def update_tutoria(
    data: TutoriaUpdate,
    tutoria: Tutoria = Depends(get_tutoria_or_404),
    session: Session = Depends(get_session)
):
    return tutoria_service.update_tutoria(db=session, tutoria=tutoria, data=data)


# 🔹 Eliminar tutoría
@router.delete("/{id_tutoria}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tutoria(tutoria: Tutoria = Depends(get_tutoria_or_404), session: Session = Depends(get_session)):
    session.delete(tutoria)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# === Endpoints Específicos ===

# 🔹 Obtener todas las tutorías de un alumno
@router.get("/alumno/{id_alumno}", response_model=List[TutoriaReadWithDetails])
def get_tutorias_by_alumno(id_alumno: int, session: Session = Depends(get_session)):
    # ✅ Práctica estándar: Devolver una lista vacía si no hay resultados, no un 404.
    tutorias = session.exec(select(Tutoria).where(Tutoria.alumno_id == id_alumno)).all()
    return tutorias


# 🔹 Obtener tutorías de un tutor (filtradas por estado activo/inactivo)
@router.get("/tutor/{id_tutor}", response_model=List[TutoriaReadWithDetails])
def get_tutorias_by_tutor(id_tutor: int, es_activa: bool, session: Session = Depends(get_session)):
    """
    Obtiene las tutorías de un tutor, filtrando por si están activas o no.
    Uso: /tutorias/tutor/1?es_activa=true
    """
    tutorias = session.exec(
        select(Tutoria).where(Tutoria.tutor_id == id_tutor, Tutoria.es_activa == es_activa)
    ).all()
    return tutorias