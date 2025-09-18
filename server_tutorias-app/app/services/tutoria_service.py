# app/services/tutoria_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.tutoria import Tutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate
from app.models.alumno import Alumno
from app.models.tutor import Tutor


def create_tutoria(db: Session, data: TutoriaCreate) -> Tutoria:
    """Crea una nueva tutoría con validaciones de reglas de negocio."""
    
    # 1. Validar que el alumno exista
    alumno = db.get(Alumno, data.alumno_id)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El alumno especificado no existe.")

    # 2. Validar que el tutor exista (si se proporciona)
    if data.tutor_id:
        tutor = db.get(Tutor, data.tutor_id)
        if not tutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tutor especificado no existe.")

    # 3. Regla de negocio: Máximo 4 tutorías por alumno
    tutorias_existentes = db.exec(
        select(Tutoria).where(Tutoria.alumno_id == data.alumno_id)
    ).all()
    
    if len(tutorias_existentes) >= 4:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El alumno ya tiene el máximo de 4 tutorías asignadas."
        )
    
    # 4. Regla de negocio: Periodo único por alumno (si se proporciona)
    if data.periodo:
        periodo_existente = db.exec(
            select(Tutoria).where(Tutoria.alumno_id == data.alumno_id, Tutoria.periodo == data.periodo)
        ).first()
        if periodo_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El periodo '{data.periodo}' ya ha sido asignado a este alumno."
            )
    
    tutoria = Tutoria.model_validate(data.model_dump())
    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    return tutoria


def update_tutoria(db: Session, tutoria: Tutoria, data: TutoriaUpdate) -> Tutoria:
    """Actualiza una tutoría existente."""
    
    # Validar que el nuevo tutor exista (si se cambia)
    if data.tutor_id:
        tutor = db.get(Tutor, data.tutor_id)
        if not tutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tutor especificado no existe.")
            
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tutoria, key, value)
    
    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    return tutoria