# app/services/alumno_service.py

from fastapi import HTTPException, status, UploadFile
from sqlmodel import Session, select, delete, func
import pandas as pd

from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate, AlumnoSetPassword, AlumnoUpdatePassword, AlumnoTutoriaStatus
from app.models.tutoria import Tutoria, EstadoTutoria # Sigue siendo necesario para imports si se usan relaciones
from app.database import engine
from app.core.security import get_password_hash, verify_password

# --- Funciones de Servicio para Alumno ---

def get_alumno_by_num_control(db: Session, num_control: str) -> Alumno | None:
    """Busca un alumno por su número de control."""
    return db.exec(select(Alumno).where(Alumno.num_control == num_control)).first()

def create_alumno(db: Session, data: AlumnoCreate) -> Alumno:
    """Crea un nuevo alumno (sin tutorías por defecto)."""
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
    """Actualiza los datos de un alumno."""
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

def process_and_load_excel(db: Session, file: UploadFile):
    """
    Procesa Excel, valida datos, borra alumnos y carga los nuevos
    con contraseña temporal (SIN CURP).
    """
    try:
        # ✅ Mapa de columnas actualizado SIN CURP
        column_map = {
            "numero_control": "num_control", "nombre": "nombre",
            "apellido_paterno": "apellido_p", "apellido_materno": "apellido_m",
            "carrera": "carrera", "semestre": "semestre_actual",
            "estatus": "estado", "email": "correo" # Asumiendo que Excel usa 'correo' ahora
        }

        # Asumiendo que el Excel ya no tiene columna 'curp'
        df = pd.read_excel(file.file, dtype={'numero_control': str}) # Quitamos dtype de curp
        df.rename(columns=column_map, inplace=True)
        df = df.astype(object).where(pd.notnull(df), None)

        # Normalización de texto
        name_columns = ['nombre', 'apellido_p', 'apellido_m']
        for col in name_columns:
            if col in df.columns: df[col] = df[col].str.title()
        if 'carrera' in df.columns:
            df['carrera'] = df['carrera'].str.title().str.replace(" En ", " en ")
        if 'correo' in df.columns: df['correo'] = df['correo'].str.lower()

        # ✅ Validación de columnas obligatorias actualizada SIN CURP
        required_columns = ['num_control', 'nombre', 'apellido_p', 'carrera', 'semestre_actual', 'correo']
        null_check = df[required_columns].isnull()
        if null_check.any().any():
            first_error_row = df[null_check.any(axis=1)].iloc[0]
            raise HTTPException(
                status_code=400,
                detail=f"Error de datos: Faltan valores obligatorios. Revise al alumno '{first_error_row['num_control']}'.")

        alumnos_a_crear = []
        for _, row in df.iterrows():
            row_data = row.to_dict()
            if 'estado' not in row_data and 'estatus' in row_data:
                row_data['estado'] = row_data.pop('estatus')
            row_data["contraseña"] = f'{row_data["num_control"]}itsf'
            # ✅ La creación del Alumno ya no espera 'curp'
            alumnos_a_crear.append(Alumno(**row_data))

        db.execute(delete(Alumno))
        db.add_all(alumnos_a_crear)
        db.commit()

        return len(alumnos_a_crear)

    except KeyError as e:
        db.rollback()
        # ✅ Mensaje de error más genérico si falta una columna mapeada
        raise HTTPException(status_code=400, detail=f"Columna '{e}' esperada no encontrada en Excel o en el mapeo.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")


def set_permanent_password(db: Session, data: AlumnoSetPassword):
    """Establece contraseña permanente para un alumno con temporal."""
    alumno = get_alumno_by_num_control(db, data.num_control)
    if not alumno: raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    if not alumno.requires_password_change:
        raise HTTPException(status_code=400, detail="Este alumno ya tiene contraseña permanente.")
    if data.contraseña_actual != alumno.contraseña:
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    alumno.requires_password_change = False
    db.add(alumno)
    db.commit()
    return {"message": "Contraseña actualizada exitosamente."}

def change_password(db: Session, alumno: Alumno, data: AlumnoUpdatePassword):
    """Permite a un alumno con contraseña permanente cambiarla."""
    if alumno.requires_password_change:
        raise HTTPException(status_code=400, detail="Debe usar /set-password primero.")
    if not verify_password(data.contraseña_actual, alumno.contraseña):
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")
    hashed_password = get_password_hash(data.nueva_contraseña)
    alumno.contraseña = hashed_password
    db.add(alumno)
    db.commit()
    return {"message": "Su contraseña ha sido actualizada exitosamente."}

def get_alumno_tutoria_status(db: Session, id_alumno: int) -> AlumnoTutoriaStatus:
    """
    Calcula el estado de las tutorías de un alumno para
    determinar si es elegible para su constancia.
    """
    # 1. Contar cuántas tutorías tiene este alumno con estado "COMPLETADA"
    query = select(func.count(Tutoria.id_tutoria)).where( # type: ignore
        Tutoria.alumno_id == id_alumno,
        Tutoria.estado == EstadoTutoria.COMPLETADA
    )
    count = db.exec(query).one()

    # 2. Definir la regla de negocio (4 o más)
    es_elegible = count >= 1

    # 3. Devolver el objeto de respuesta
    return AlumnoTutoriaStatus(tutorias_completadas=count, es_elegible=es_elegible)