"""
Servicio de lógica de negocio para la gestión de Alumnos.

Proporciona funciones para operaciones CRUD, autenticación, gestión de contraseñas
y procesamiento de carga masiva desde archivos Excel.
"""

from fastapi import HTTPException, status, UploadFile
from sqlmodel import Session, select, delete, func
import pandas as pd

from app.models.alumno import Alumno
from app.schemas.alumno import (
    AlumnoCreate, 
    AlumnoUpdate, 
    AlumnoSetPassword, 
    AlumnoUpdatePassword, 
    AlumnoTutoriaStatus
)
from app.models.tutoria import Tutoria, EstadoTutoria
from app.core.security import get_password_hash, verify_password


def get_alumno_by_num_control(db: Session, num_control: str) -> Alumno | None:
    """
    Busca un alumno por su número de control único.
    """
    return db.exec(select(Alumno).where(Alumno.num_control == num_control)).first()


def create_alumno(db: Session, data: AlumnoCreate) -> Alumno:
    """
    Crea un nuevo alumno en el sistema.
    """
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
    db.refresh(alumno)
    
    return alumno


def update_alumno(db: Session, alumno: Alumno, data: AlumnoUpdate) -> Alumno:
    """
    Actualiza los datos de un alumno existente.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    if "contraseña" in update_data:
        new_password = update_data["contraseña"]
        
        if new_password:
            # --- CORRECCIÓN CRÍTICA ---
            # Si el Admin cambia la contraseña, la hasheamos Y desactivamos la bandera
            # de cambio obligatorio, asumiendo que el Admin estableció una contraseña válida.
            update_data["contraseña"] = get_password_hash(new_password)
            update_data["requires_password_change"] = False 
        else:
            del update_data["contraseña"]
    
    for key, value in update_data.items():
        setattr(alumno, key, value)
    
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    
    return alumno


def process_and_load_excel(db: Session, file: UploadFile) -> int:
    """
    Procesa y carga alumnos desde un archivo Excel.
    """
    try:
        column_map = {
            "numero_control": "num_control",
            "nombre": "nombre",
            "apellido_paterno": "apellido_p",
            "apellido_materno": "apellido_m",
            "carrera": "carrera",
            "semestre": "semestre_actual",
            "estatus": "estado",
            "email": "correo"
        }
        
        df = pd.read_excel(file.file, dtype={'numero_control': str})
        df.rename(columns=column_map, inplace=True)
        df = df.astype(object).where(pd.notnull(df), None)
        
        name_columns = ['nombre', 'apellido_p', 'apellido_m']
        for col in name_columns:
            if col in df.columns:
                df[col] = df[col].str.title()
        
        if 'carrera' in df.columns:
            df['carrera'] = df['carrera'].str.title().str.replace(" En ", " en ")
        
        if 'correo' in df.columns:
            df['correo'] = df['correo'].str.lower()
        
        required_columns = ['num_control', 'nombre', 'apellido_p', 'carrera', 'semestre_actual', 'correo']
        null_check = df[required_columns].isnull()
        
        if null_check.any().any():
            first_error_row = df[null_check.any(axis=1)].iloc[0]
            raise HTTPException(
                status_code=400,
                detail=f"Error de datos: Faltan valores obligatorios. Revise al alumno '{first_error_row['num_control']}'."
            )
        
        alumnos_a_crear = []
        
        for _, row in df.iterrows():
            row_data = row.to_dict()
            
            if 'estado' not in row_data and 'estatus' in row_data:
                row_data['estado'] = row_data.pop('estatus')
            
            # Contraseña temporal en texto plano (flag requires_password_change=True por defecto en modelo)
            row_data["contraseña"] = f'{row_data["num_control"]}itsf'
            alumnos_a_crear.append(Alumno(**row_data))
        
        db.execute(delete(Alumno))
        db.add_all(alumnos_a_crear)
        db.commit()
        
        return len(alumnos_a_crear)
    
    except KeyError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Columna '{e}' esperada no encontrada en Excel o en el mapeo."
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar archivo: {str(e)}"
        )


def set_permanent_password(db: Session, data: AlumnoSetPassword) -> dict:
    """
    Establece una contraseña permanente para un alumno con contraseña temporal.
    """
    alumno = get_alumno_by_num_control(db, data.num_control)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    
    if not alumno.requires_password_change:
        raise HTTPException(
            status_code=400,
            detail="Este alumno ya tiene contraseña permanente."
        )
    
    # Validación Robusta: Intentamos comparar texto plano O verificar hash
    # Esto cubre el caso donde un Admin reseteó la pass pero la flag quedó True (casos viejos)
    is_valid = False
    if data.contraseña_actual == alumno.contraseña: # Caso Excel (Texto plano)
        is_valid = True
    elif verify_password(data.contraseña_actual, alumno.contraseña): # Caso Admin Reset (Hash)
        is_valid = True
        
    if not is_valid:
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    alumno.requires_password_change = False
    
    db.add(alumno)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente."}


def change_password(db: Session, alumno: Alumno, data: AlumnoUpdatePassword) -> dict:
    """
    Cambia la contraseña de un alumno autenticado.
    """
    if alumno.requires_password_change:
        raise HTTPException(
            status_code=400,
            detail="Debe usar /set-password primero."
        )
    
    if not verify_password(data.contraseña_actual, alumno.contraseña):
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    
    db.add(alumno)
    db.commit()
    
    return {"message": "Su contraseña ha sido actualizada exitosamente."}


def get_alumno_tutoria_status(db: Session, id_alumno: int) -> AlumnoTutoriaStatus:
    """
    Obtiene el estado de progreso de tutorías de un alumno.
    """
    query = select(func.count(Tutoria.id_tutoria)).where(  # type: ignore
        Tutoria.alumno_id == id_alumno,
        Tutoria.estado == EstadoTutoria.COMPLETADA
    )
    
    count = db.exec(query).one()
    es_elegible = count >= 1
    
    return AlumnoTutoriaStatus(
        tutorias_completadas=count,
        es_elegible=es_elegible
    )