# app/services/alumno_service.py

from fastapi import HTTPException, status, UploadFile
from sqlmodel import Session, select, delete
from passlib.context import CryptContext
import pandas as pd

from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate, AlumnoSetPassword
from app.models.tutoria import Tutoria
from app.database import engine

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
    
    alumno = Alumno.model_validate(
        data.model_dump(), 
        update={
            'contraseña': hashed_password,
            'requires_password_change': False 
        }
    )
    
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

def process_and_load_excel(db: Session, file: UploadFile):
    """
    Procesa un archivo Excel, valida los datos, borra los alumnos existentes 
    y carga los nuevos con una contraseña temporal.
    """
    try:
        column_map = {
            "numero_control": "num_control", "nombre": "nombre",
            "apellido_paterno": "apellido_p", "apellido_materno": "apellido_m",
            "carrera": "carrera", "semestre": "semestre_actual",
            "curp": "curp", "estatus": "estado", "email": "correo"
        }
        
        df = pd.read_excel(file.file, dtype={'numero_control': str, 'curp': str})
        df.rename(columns=column_map, inplace=True)
        df = df.astype(object).where(pd.notnull(df), None)
        
        # ... (limpieza de texto) ...
        text_columns = ['nombre', 'apellido_p', 'apellido_m', 'carrera']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].str.title()
        if 'correo' in df.columns:
            df['correo'] = df['correo'].str.lower()

        # ✅ NUEVA VALIDACIÓN: Revisar que las columnas obligatorias no tengan valores nulos
        required_columns = ['num_control', 'nombre', 'apellido_p', 'carrera', 'semestre_actual', 'curp', 'correo']
        null_check = df[required_columns].isnull()
        if null_check.any().any():
            # (Opcional) Encontrar la primera fila con error para un mensaje más útil
            first_error_row = df[null_check.any(axis=1)].iloc[0]
            raise HTTPException(
                status_code=400,
                detail=f"Error de datos: El archivo contiene filas con valores vacíos en columnas obligatorias. "
                        f"Por ejemplo, el alumno con número de control '{first_error_row['num_control']}' tiene datos faltantes. "
                        "Por favor, revise el archivo."
            )

        alumnos_a_crear = []
        for _, row in df.iterrows():
            row_data = row.to_dict()
            row_data["contraseña"] = f'{row_data["num_control"]}itsf'
            alumnos_a_crear.append(Alumno(**row_data))

        db.execute(delete(Alumno))
        db.add_all(alumnos_a_crear)
        db.commit()

        return len(alumnos_a_crear)

    except KeyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"La columna requerida {e} no se encontró en el Excel.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    
def set_permanent_password(db: Session, data: AlumnoSetPassword):
    """
    Establece una contraseña permanente y hasheada para un alumno
    que actualmente tiene una contraseña temporal.
    """
    # 1. Buscar al alumno por su número de control
    alumno = get_alumno_by_num_control(db, data.num_control)
    if not alumno:
        raise HTTPException(status_code=404, detail="El alumno no fue encontrado.")

    # 2. Verificar que el alumno realmente necesite un cambio de contraseña
    if not alumno.requires_password_change:
        raise HTTPException(
            status_code=400, 
            detail="Este alumno ya tiene una contraseña permanente."
        )
        
    # 3. Validar que la contraseña actual (temporal) sea correcta
    if data.contraseña_actual != alumno.contraseña:
        raise HTTPException(
            status_code=401,
            detail="La contraseña actual es incorrecta."
        )

    # 4. Hashear y actualizar la nueva contraseña
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    alumno.requires_password_change = False # 👈 Cambiamos la bandera

    db.add(alumno)
    db.commit()

    return {"message": "Contraseña actualizada exitosamente."}