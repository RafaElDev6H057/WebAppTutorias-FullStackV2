# app/services/tutor_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select

# ✅ 1. Importaciones de seguridad corregidas
from app.core.security import get_password_hash, verify_password

from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate

def get_tutor_by_email(db: Session, email: str) -> Tutor | None:
    """Busca un tutor por su correo electrónico."""
    return db.exec(select(Tutor).where(Tutor.correo == email)).first()

def create_tutor(db: Session, data: TutorCreate) -> Tutor:
    """Crea un nuevo tutor en la base de datos."""
    
    db_tutor = get_tutor_by_email(db, data.correo)
    if db_tutor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El correo '{data.correo}' ya está registrado."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    
    # ✅ 2. Lógica de creación actualizada
    # Establecemos la contraseña hasheada y la bandera en False
    tutor = Tutor.model_validate(
        data.model_dump(), 
        update={
            'contraseña': hashed_password,
            'requires_password_change': False
        }
    )
    
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor

def update_tutor(db: Session, tutor: Tutor, data: TutorUpdate) -> Tutor:
    """Actualiza los datos de un tutor."""
    update_data = data.model_dump(exclude_unset=True)

    if "contraseña" in update_data:
        new_password = update_data["contraseña"]
        
        if new_password:
            update_data["contraseña"] = get_password_hash(new_password)
        else:
            del update_data["contraseña"]
    
    for key, value in update_data.items():
        setattr(tutor, key, value)
    
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor