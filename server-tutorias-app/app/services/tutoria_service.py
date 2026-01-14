"""
Servicio de lógica de negocio para la gestión de Tutorías.

Proporciona funciones para operaciones CRUD, procesamiento de asignaciones
desde archivos CSV y validación de reglas de negocio de tutorías.
"""

from fastapi import HTTPException, status, UploadFile
from sqlmodel import Session, select
import pandas as pd
from io import StringIO
from typing import Optional

from app.models.tutoria import Tutoria, EstadoTutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate
from app.models.alumno import Alumno
from app.models.tutor import Tutor
from . import tutor_service
from . import alumno_service


def create_tutoria(db: Session, data: TutoriaCreate) -> Tutoria:
    """
    Crea una nueva tutoría manualmente.
    
    Valida la existencia del alumno y tutor, verifica que el alumno no exceda
    el máximo histórico de tutorías (4) y que no tenga duplicados para el mismo periodo.
    
    Args:
        db: Sesión de base de datos.
        data: Datos de la tutoría a crear.
    
    Returns:
        Instancia de la tutoría creada.
    
    Raises:
        HTTPException: Si el alumno o tutor no existe, si se excede el límite
                      de tutorías o si ya existe una tutoría para ese periodo.
    """
    alumno = db.get(Alumno, data.alumno_id)
    
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El alumno especificado no existe."
        )
    
    if data.tutor_id:
        tutor = db.get(Tutor, data.tutor_id)
        
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tutor especificado no existe."
            )
    
    tutorias_existentes = db.exec(
        select(Tutoria).where(Tutoria.alumno_id == data.alumno_id)
    ).all()
    
    if len(tutorias_existentes) >= 4:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El alumno ya tiene el máximo histórico de 4 tutorías."
        )
    
    if data.periodo:
        periodo_existente = db.exec(
            select(Tutoria).where(
                Tutoria.alumno_id == data.alumno_id,
                Tutoria.periodo == data.periodo
            )
        ).first()
        
        if periodo_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El alumno ya tiene una tutoría asignada para el periodo '{data.periodo}'."
            )
    
    tutoria = Tutoria.model_validate(data.model_dump())
    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    
    return tutoria


def update_tutoria(db: Session, tutoria: Tutoria, data: TutoriaUpdate) -> Tutoria:
    """
    Actualiza una tutoría existente.
    
    Si se proporciona un nuevo tutor_id, valida que el tutor exista.
    
    Args:
        db: Sesión de base de datos.
        tutoria: Instancia de la tutoría a actualizar.
        data: Datos actualizados de la tutoría.
    
    Returns:
        Instancia de la tutoría actualizada.
    
    Raises:
        HTTPException: Si el tutor especificado no existe.
    """
    if data.tutor_id is not None:
        tutor = db.get(Tutor, data.tutor_id)
        
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tutor especificado no existe."
            )
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(tutoria, key, value)
    
    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    
    return tutoria


def process_assignment_csv(db: Session, file: UploadFile) -> dict:
    """
    Procesa un archivo CSV de asignación de tutorías y crea registros masivos.
    
    El archivo CSV debe contener:
    - Metadata en las primeras 9 filas (incluyendo periodo y nombre del tutor)
    - Tabla de alumnos a partir de la fila 10 con columna 'NoControl'
    
    Formato esperado de metadata:
        - Fila 7 (índice 6): "PERIODO [periodo]"
        - Fila 8 (índice 7): "DOCENTE [nombre completo]"
    
    Args:
        db: Sesión de base de datos.
        file: Archivo CSV cargado con formato de asignación.
    
    Returns:
        Diccionario con resumen del procesamiento: tutorías creadas, alumnos no encontrados
        y lista de errores o advertencias.
    
    Raises:
        HTTPException: Si hay errores de formato, el tutor no existe o error de procesamiento.
    """
    processed_count = 0
    skipped_alumnos_not_found = 0
    errors = []
    
    try:
        content_bytes = file.file.read()
        content_str = content_bytes.decode('latin1')
        file_stream = StringIO(content_str)
        
        file_stream.seek(0)
        metadata_df = pd.read_csv(file_stream, header=None, nrows=9, encoding='latin1')
        
        try:
            periodo_raw = metadata_df.iloc[6, 0]
            periodo = str(periodo_raw).replace("PERIODO ", "").strip()
            
            tutor_name_raw = metadata_df.iloc[7, 0]
            tutor_full_name = str(tutor_name_raw).replace("DOCENTE ", "").strip()
        except (IndexError, AttributeError):
            raise HTTPException(
                status_code=400,
                detail="Error al leer la metadata del CSV. Formato inesperado."
            )
        
        tutor = tutor_service.get_tutor_by_full_name_case_insensitive(db, tutor_full_name)
        
        if not tutor:
            raise HTTPException(
                status_code=404,
                detail=f"Tutor '{tutor_full_name}' no encontrado en la base de datos."
            )
        
        file_stream.seek(0)
        
        try:
            students_df = pd.read_csv(
                file_stream,
                skiprows=9,
                encoding='latin1',
                dtype={'NoControl': str}
            )
        except pd.errors.EmptyDataError:
            return {
                "message": f"Archivo '{file.filename}' procesado. No se encontraron alumnos.",
                "nuevas_tutorias_creadas": 0,
                "alumnos_no_encontrados": 0
            }
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail="Columna 'NoControl' no encontrada en la tabla de alumnos del CSV."
            )
        
        for index, row in students_df.iterrows():
            current_row_number = int(index) + 11 #type:ignore
            
            if pd.isna(row['NoControl']) or not str(row['NoControl']).strip():
                errors.append(f"Fila {current_row_number}: Número de control vacío.")
                continue
            
            num_control = str(row['NoControl']).strip()
            alumno = alumno_service.get_alumno_by_num_control(db, num_control)
            
            if not alumno:
                skipped_alumnos_not_found += 1
                errors.append(
                    f"Fila {current_row_number}: Alumno con NoControl '{num_control}' no encontrado."
                )
                continue
            
            existing_tutoria: Optional[Tutoria] = db.exec(
                select(Tutoria).where(
                    Tutoria.alumno_id == alumno.id_alumno,
                    Tutoria.periodo == periodo
                )
            ).first()
            
            if existing_tutoria:
                errors.append(
                    f"Fila {current_row_number}: Alumno '{num_control}' ya tiene tutoría "
                    f"para el periodo '{periodo}'."
                )
                continue
            
            if tutor.id_tutor is None:
                errors.append(
                    f"Error interno: ID del tutor '{tutor_full_name}' no encontrado "
                    f"después de la búsqueda."
                )
                continue
            
            if alumno.id_alumno is None:
                errors.append(
                    f"Error interno: ID del alumno '{num_control}' no encontrado "
                    f"después de la búsqueda."
                )
                continue
            
            nueva_tutoria = Tutoria(
                alumno_id=alumno.id_alumno,
                tutor_id=tutor.id_tutor,
                periodo=periodo,
                semestre=alumno.semestre_actual,
                estado=EstadoTutoria.PENDIENTE
            )
            
            db.add(nueva_tutoria)
            processed_count += 1
        
        db.commit()
        
        summary = {
            "message": f"Archivo '{file.filename}' procesado.",
            "tutor_asignado": tutor_full_name,
            "periodo": periodo,
            "nuevas_tutorias_creadas": processed_count,
            "alumnos_no_encontrados": skipped_alumnos_not_found,
            "filas_csv_ignoradas": len(students_df) - processed_count - skipped_alumnos_not_found
        }
        
        if errors:
            summary["detalles_saltados_o_errores"] = errors
        
        return summary
    
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al procesar el archivo '{file.filename}'."
        )
