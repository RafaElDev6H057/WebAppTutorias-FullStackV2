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
    
    Args:
        db: Sesión de base de datos.
        email: Correo electrónico del tutor a buscar.
    
    Returns:
        Instancia de Tutor si existe, None en caso contrario.
    """
    return db.exec(select(Tutor).where(Tutor.correo == email)).first()


def get_tutor_by_full_name_case_insensitive(db: Session, csv_full_name: str) -> Tutor | None:
    """
    Busca un tutor comparando su nombre completo de forma no sensible a mayúsculas.
    
    Construye el nombre completo del tutor (nombre + apellido paterno + apellido materno)
    y lo compara con el nombre proporcionado, ignorando diferencias en mayúsculas/minúsculas
    y espacios extra.
    
    Args:
        db: Sesión de base de datos.
        csv_full_name: Nombre completo del tutor a buscar (usualmente extraído de CSV).
    
    Returns:
        Instancia de Tutor si se encuentra coincidencia, None en caso contrario.
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
    
    Args:
        db: Sesión de base de datos.
        data: Datos del tutor a crear.
    
    Returns:
        Instancia del tutor creado.
    
    Raises:
        HTTPException: Si el correo electrónico ya está registrado.
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
    
    Si se proporciona una nueva contraseña, esta será hasheada antes de guardarse.
    
    Args:
        db: Sesión de base de datos.
        tutor: Instancia del tutor a actualizar.
        data: Datos actualizados del tutor.
    
    Returns:
        Instancia del tutor actualizado.
    """
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


def set_permanent_password(db: Session, data: TutorSetPassword) -> dict:
    """
    Establece una contraseña permanente para un tutor con contraseña temporal.
    
    El tutor debe proporcionar su contraseña temporal actual para
    poder establecer una nueva contraseña permanente.
    
    Args:
        db: Sesión de base de datos.
        data: Datos de establecimiento de contraseña (correo, contraseña actual y nueva).
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el tutor no existe, la contraseña actual es incorrecta
                    o el tutor ya tiene contraseña permanente.
    """
    tutor = get_tutor_by_email(db, data.correo)
    
    if not tutor:
        raise HTTPException(status_code=404, detail="El tutor no fue encontrado.")
    
    if not tutor.requires_password_change:
        raise HTTPException(
            status_code=400,
            detail="Este tutor ya tiene una contraseña permanente."
        )
    
    if data.contraseña_actual != tutor.contraseña:
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
    
    Args:
        db: Sesión de base de datos.
        tutor: Instancia del tutor autenticado.
        data: Datos de cambio de contraseña (contraseña actual y nueva).
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el tutor aún requiere establecer contraseña inicial
                    o la contraseña actual es incorrecta.
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
