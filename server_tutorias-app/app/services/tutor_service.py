# app/services/tutor_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select

# 💡 Pro Tip: Las funciones de contraseña se repiten en alumno_service.
# A futuro, podrías moverlas a un archivo común como `app/core/security.py`
# para no repetir código. Por ahora, las mantenemos aquí por claridad.
from app.services.alumno_service import get_password_hash, verify_password

from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate

def get_tutor_by_email(db: Session, email: str) -> Tutor | None:
    """Busca un tutor por su correo electrónico."""
    return db.exec(select(Tutor).where(Tutor.correo == email)).first()

def create_tutor(db: Session, data: TutorCreate) -> Tutor:
    """Crea un nuevo tutor en la base de datos."""
    # ✅ 1. Verificamos si ya existe un tutor con ese correo
    db_tutor = get_tutor_by_email(db, data.correo)
    if db_tutor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El correo '{data.correo}' ya está registrado."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    
    # Usamos .model_validate() para crear el objeto del modelo
    tutor = Tutor.model_validate(data.model_dump(), update={'contraseña': hashed_password})
    
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor

def update_tutor(db: Session, tutor: Tutor, data: TutorUpdate) -> Tutor:
    """Actualiza los datos de un tutor."""
    update_data = data.model_dump(exclude_unset=True)

    # ✅ Manejo especial y explícito de la contraseña
    if "contraseña" in update_data:
        new_password = update_data["contraseña"]
        
        # Si se proporcionó una nueva contraseña (no es None ni un string vacío)
        if new_password:
            update_data["contraseña"] = get_password_hash(new_password)
        # Si la contraseña es None o un string vacío ""
        else:
            # La eliminamos del diccionario para que no se actualice en la base de datos
            del update_data["contraseña"]
    
    for key, value in update_data.items():
        setattr(tutor, key, value)
    
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor