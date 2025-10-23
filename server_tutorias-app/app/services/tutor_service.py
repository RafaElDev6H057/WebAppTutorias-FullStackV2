# app/services/tutor_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select

# ✅ Imports correctos
from app.core.security import get_password_hash, verify_password

from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate, TutorSetPassword, TutorUpdatePassword

def get_tutor_by_email(db: Session, email: str) -> Tutor | None:
    """Busca un tutor por su correo electrónico."""
    return db.exec(select(Tutor).where(Tutor.correo == email)).first()

def get_tutor_by_full_name_case_insensitive(db: Session, csv_full_name: str) -> Tutor | None:
    """
    Busca un tutor en la base de datos comparando su nombre completo
    (nombre + apellidos) de forma no sensible a mayúsculas/minúsculas.

    Args:
        db: La sesión de la base de datos.
        csv_full_name: El nombre completo del tutor extraído del archivo CSV.

    Returns:
        El objeto Tutor si se encuentra una coincidencia, de lo contrario None.
    """
    # 1. Normalizamos el nombre del CSV a mayúsculas y quitamos espacios extra
    normalized_csv_name = ' '.join(csv_full_name.upper().split())

    # 2. Obtenemos todos los tutores de la base de datos
    all_tutores = db.exec(select(Tutor)).all()

    # 3. Iteramos y comparamos nombres
    for tutor in all_tutores:
        # Construimos el nombre completo desde la base de datos
        db_name_parts = [tutor.nombre, tutor.apellido_p]
        if tutor.apellido_m:
            db_name_parts.append(tutor.apellido_m)
        
        # Normalizamos el nombre de la BD igual que el del CSV
        db_full_name = " ".join(part for part in db_name_parts if part) # Une solo si no es None/vacío
        normalized_db_name = ' '.join(db_full_name.upper().split())

        # Comparamos
        if normalized_db_name == normalized_csv_name:
            return tutor # ¡Encontrado!

    # Si el bucle termina sin encontrar coincidencia
    return None

def create_tutor(db: Session, data: TutorCreate) -> Tutor:
    """Crea un nuevo tutor en la base de datos (por un admin)."""
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
    """Actualiza los datos de un tutor (por un admin)."""
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

def set_permanent_password(db: Session, data: TutorSetPassword):
    """Establece la contraseña inicial hasheada para un tutor."""
    tutor = get_tutor_by_email(db, data.correo)
    if not tutor:
        raise HTTPException(status_code=404, detail="El tutor no fue encontrado.")
    if not tutor.requires_password_change:
        raise HTTPException(status_code=400, detail="Este tutor ya tiene una contraseña permanente.")
    if data.contraseña_actual != tutor.contraseña:
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    hashed_password = get_password_hash(data.nueva_contraseña)
    tutor.contraseña = hashed_password
    tutor.requires_password_change = False
    db.add(tutor)
    db.commit()
    return {"message": "Contraseña actualizada exitosamente."}

def change_password(db: Session, tutor: Tutor, data: TutorUpdatePassword):
    """Permite a un tutor cambiar su contraseña hasheada existente."""
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