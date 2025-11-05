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
    
    Args:
        db: Sesión de base de datos.
        num_control: Número de control del alumno a buscar.
    
    Returns:
        Instancia de Alumno si existe, None en caso contrario.
    """
    return db.exec(select(Alumno).where(Alumno.num_control == num_control)).first()


def create_alumno(db: Session, data: AlumnoCreate) -> Alumno:
    """
    Crea un nuevo alumno en el sistema.
    
    Args:
        db: Sesión de base de datos.
        data: Datos del alumno a crear.
    
    Returns:
        Instancia del alumno creado.
    
    Raises:
        HTTPException: Si el número de control ya está registrado.
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
    
    Si se proporciona una nueva contraseña, esta será hasheada antes de guardarse.
    
    Args:
        db: Sesión de base de datos.
        alumno: Instancia del alumno a actualizar.
        data: Datos actualizados del alumno.
    
    Returns:
        Instancia del alumno actualizado.
    """
    update_data = data.model_dump(exclude_unset=True)
    
    if "contraseña" in update_data:
        new_password = update_data["contraseña"]
        
        if new_password:
            update_data["contraseña"] = get_password_hash(new_password)
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
    
    Este proceso elimina todos los alumnos existentes y los reemplaza
    con los datos del archivo. Los alumnos son creados con contraseñas
    temporales basadas en su número de control.
    
    Formato esperado del Excel:
        - numero_control: Número de control del alumno
        - nombre: Nombre(s)
        - apellido_paterno: Apellido paterno
        - apellido_materno: Apellido materno (opcional)
        - carrera: Nombre de la carrera
        - semestre: Semestre actual
        - estatus: Estado del alumno
        - email: Correo electrónico
    
    Args:
        db: Sesión de base de datos.
        file: Archivo Excel cargado.
    
    Returns:
        Número de alumnos cargados exitosamente.
    
    Raises:
        HTTPException: Si hay errores de validación o procesamiento.
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
    
    El alumno debe proporcionar su contraseña temporal actual para
    poder establecer una nueva contraseña permanente.
    
    Args:
        db: Sesión de base de datos.
        data: Datos de establecimiento de contraseña (num_control, contraseña actual y nueva).
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el alumno no existe, la contraseña actual es incorrecta
                    o el alumno ya tiene contraseña permanente.
    """
    alumno = get_alumno_by_num_control(db, data.num_control)
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    
    if not alumno.requires_password_change:
        raise HTTPException(
            status_code=400,
            detail="Este alumno ya tiene contraseña permanente."
        )
    
    if data.contraseña_actual != alumno.contraseña:
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    alumno.requires_password_change = False
    
    db.add(alumno)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente."}


def change_password(db: Session, alumno: Alumno, data: AlumnoUpdatePassword) -> dict:
    """
    Cambia la contraseña de un alumno autenticado que ya tiene contraseña permanente.
    
    Args:
        db: Sesión de base de datos.
        alumno: Instancia del alumno autenticado.
        data: Datos de cambio de contraseña (contraseña actual y nueva).
    
    Returns:
        Diccionario con mensaje de confirmación.
    
    Raises:
        HTTPException: Si el alumno aún requiere establecer contraseña inicial
                    o la contraseña actual es incorrecta.
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
    
    Calcula el número de tutorías completadas y determina si el alumno
    es elegible para obtener su constancia de tutorías.
    
    Args:
        db: Sesión de base de datos.
        id_alumno: Identificador del alumno.
    
    Returns:
        Estado de tutorías del alumno con contador y elegibilidad.
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
