# app/services/alumno_service.py

from fastapi import HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate
from app.models.tutoria import Tutoria

# Mueve el contexto de la contraseña aquí, ya que es parte de la lógica de negocio
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_alumno_by_num_control(db: Session, num_control: str) -> Alumno | None:
    """Busca un alumno por su número de control."""
    return db.exec(select(Alumno).where(Alumno.num_control == num_control)).first()

def create_alumno(db: Session, data: AlumnoCreate) -> Alumno:
    """Crea un nuevo alumno y sus 4 tutorías base por defecto."""
    
    # Verificamos si ya existe un alumno con ese número de control
    db_alumno = get_alumno_by_num_control(db, data.num_control)
    if db_alumno:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El número de control '{data.num_control}' ya está registrado."
        )
    
    hashed_password = get_password_hash(data.contraseña)
    
    alumno = Alumno.model_validate(data.model_dump(), update={'contraseña': hashed_password})
    
    db.add(alumno)
    db.commit()
    db.refresh(alumno) # En este punto, `alumno.id_alumno` ya está disponible

    # ✅ 2. Lógica para crear las 4 tutorías base
    if alumno.id_alumno is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo obtener el id_alumno después de crear el alumno."
        )
    for semestre_tutoria in range(1, 5):
        tutoria_base = Tutoria(
            alumno_id=alumno.id_alumno,
            semestre=semestre_tutoria
            # Los demás campos (tutor_id, estado, etc.) usarán sus valores por defecto
        )
        db.add(tutoria_base)
    
    db.commit() # Guardamos las 4 nuevas tutorías en la base de datos
    db.refresh(alumno) # Opcional: refresca el objeto alumno para cargar la relación de tutorías

    return alumno

def update_alumno(db: Session, alumno: Alumno, data: AlumnoUpdate) -> Alumno:
    """Actualiza los datos de un alumno."""
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
        setattr(alumno, key, value)
    
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    return alumno