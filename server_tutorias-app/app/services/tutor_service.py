"""
Servicio de lógica de negocio para la gestión de Tutores.

Proporciona funciones para operaciones CRUD, autenticación, gestión de contraseñas
y búsqueda de tutores por nombre completo.
"""

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate, TutorSetPassword, TutorUpdatePassword


def get_tutor_by_email(db: Session, email: str) -> Tutor | None:
    """
    Busca un tutor por su dirección de correo electrónico.
    """
    return db.exec(select(Tutor).where(Tutor.correo == email)).first()


def get_tutor_by_full_name_case_insensitive(db: Session, csv_full_name: str) -> Tutor | None:
    """
    Busca un tutor comparando su nombre completo de forma no sensible a mayúsculas.
    """
    normalized_csv_name = ' '.join(csv_full_name.upper().split())
    all_tutores = db.exec(select(Tutor)).all()
    
    for tutor in all_tutores:
        db_name_parts = [tutor.nombre, tutor.apellido_p]
        
        if tutor.apellido_m:
            db_name_parts.append(tutor.apellido_m)
        
        db_full_name = " ".join(part for part in db_name_parts if part)
        normalized_db_name = ' '.join(db_full_name.upper().split())
        
        if normalized_db_name == normalized_csv_name:
            return tutor
    
    return None


def create_tutor(db: Session, data: TutorCreate) -> Tutor:
    """
    Crea un nuevo tutor en el sistema.
    """
    db_tutor = get_tutor_by_email(db, data.correo)
    
    if db_tutor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El correo '{data.correo}' ya está registrado."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    
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
    """
    Actualiza los datos de un tutor existente.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    if "contraseña" in update_data:
        new_password = update_data["contraseña"]
        
        if new_password:
            # --- CORRECCIÓN CRÍTICA ---
            # Si el Admin actualiza la contraseña, la guardamos hasheada 
            # Y desactivamos la bandera de cambio obligatorio.
            update_data["contraseña"] = get_password_hash(new_password)
            update_data["requires_password_change"] = False
        else:
            del update_data["contraseña"]
    
    for key, value in update_data.items():
        setattr(tutor, key, value)
    
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    
    return tutor


def set_permanent_password(db: Session, data: TutorSetPassword) -> dict:
    """
    Establece una contraseña permanente para un tutor con contraseña temporal.
    """
    tutor = get_tutor_by_email(db, data.correo)
    
    if not tutor:
        raise HTTPException(status_code=404, detail="El tutor no fue encontrado.")
    
    if not tutor.requires_password_change:
        raise HTTPException(
            status_code=400,
            detail="Este tutor ya tiene una contraseña permanente."
        )
    
    # --- VALIDACIÓN ROBUSTA (Igual que en Alumnos) ---
    is_valid = False
    # 1. Intento Texto Plano (Carga masiva original)
    if data.contraseña_actual == tutor.contraseña:
        is_valid = True
    # 2. Intento Hash (Si un Admin la cambió pero la bandera seguía activa)
    elif verify_password(data.contraseña_actual, tutor.contraseña):
        is_valid = True
        
    if not is_valid:
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    
    hashed_password = get_password_hash(data.nueva_contraseña)
    tutor.contraseña = hashed_password
    tutor.requires_password_change = False
    
    db.add(tutor)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente."}


def change_password(db: Session, tutor: Tutor, data: TutorUpdatePassword) -> dict:
    """
    Cambia la contraseña de un tutor autenticado que ya tiene contraseña permanente.
    """
    if tutor.requires_password_change:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este tutor debe usar la ruta /set-password para establecer su contraseña inicial."
        )
    
    if not verify_password(data.contraseña_actual, tutor.contraseña):
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    
    hashed_password = get_password_hash(data.nueva_contraseña)
    tutor.contraseña = hashed_password
    
    db.add(tutor)
    db.commit()
    
    return {"message": "Su contraseña ha sido actualizada exitosamente."}