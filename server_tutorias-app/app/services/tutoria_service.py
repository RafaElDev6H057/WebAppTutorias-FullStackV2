# app/services/tutoria_service.py

# --- Imports ---
from fastapi import HTTPException, status, UploadFile
from sqlmodel import Session, select
import pandas as pd
from io import StringIO
from typing import Optional # Added Optional for clarity

# Models and Schemas
from app.models.tutoria import Tutoria, EstadoTutoria
from app.schemas.tutoria import TutoriaCreate, TutoriaUpdate
from app.models.alumno import Alumno
from app.models.tutor import Tutor

# Services (to find Alumno and Tutor)
from . import tutor_service
from . import alumno_service

# --- Existing Service Functions ---

def create_tutoria(db: Session, data: TutoriaCreate) -> Tutoria:
    """
    Crea una nueva tutoría manualmente (p. ej., por un admin).
    NOTA: Esta función todavía usa la lógica antigua de "máximo 4 tutorías".
    Deberíamos evaluar si esta lógica sigue siendo necesaria o si debe eliminarse
    ahora que las tutorías se basan en periodos.
    """
    # 1. Validar que el alumno exista
    alumno = db.get(Alumno, data.alumno_id)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El alumno especificado no existe.")

    # 2. Validar que el tutor exista (si se proporciona)
    if data.tutor_id:
        tutor = db.get(Tutor, data.tutor_id)
        if not tutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tutor especificado no existe.")

    # --- Consideración: ¿Sigue siendo válida esta lógica de las 4 tutorías? ---
    # Con el nuevo modelo basado en periodos, esta restricción podría ya no aplicar
    # o necesitaría ser redefinida (ej. "máximo 4 tutorías COMPLETADAS").
    # Por ahora, la dejamos como estaba.
    tutorias_existentes = db.exec(
        select(Tutoria).where(Tutoria.alumno_id == data.alumno_id)
    ).all()
    if len(tutorias_existentes) >= 4:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El alumno ya tiene el máximo histórico de 4 tutorías." # Mensaje ajustado
        )
    # --- Fin Consideración ---

    # --- Consideración: ¿Sigue siendo válida la restricción de periodo único? ---
    # Ahora que creamos una tutoría por periodo, esta validación es CRUCIAL.
    if data.periodo:
        periodo_existente = db.exec(
            select(Tutoria).where(Tutoria.alumno_id == data.alumno_id, Tutoria.periodo == data.periodo)
        ).first()
        if periodo_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El alumno ya tiene una tutoría asignada para el periodo '{data.periodo}'."
            )
    # --- Fin Consideración ---

    tutoria = Tutoria.model_validate(data.model_dump())
    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    return tutoria


def update_tutoria(db: Session, tutoria: Tutoria, data: TutoriaUpdate) -> Tutoria:
    """Actualiza una tutoría existente (p. ej., por un admin o tutor)."""
    # Validar que el nuevo tutor exista (si se cambia)
    if data.tutor_id is not None: # Check explicitly against None if 0 is a valid ID
        tutor = db.get(Tutor, data.tutor_id)
        if not tutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tutor especificado no existe.")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tutoria, key, value)

    db.add(tutoria)
    db.commit()
    db.refresh(tutoria)
    return tutoria


# --- NEW FUNCTION TO PROCESS CSV ---
def process_assignment_csv(db: Session, file: UploadFile):
    """
    Procesa UN archivo CSV de asignación de tutorías.
    Extrae metadata, busca tutor y alumnos, y CREA nuevos registros de Tutoría.
    """
    processed_count = 0
    skipped_alumnos_not_found = 0
    errors = []

    try:
        # 1. Leer el contenido del archivo en memoria
        content_bytes = file.file.read()
        content_str = content_bytes.decode('latin1')
        file_stream = StringIO(content_str)

        # 2. LEER LA METADATA
        file_stream.seek(0)
        metadata_df = pd.read_csv(file_stream, header=None, nrows=9, encoding='latin1')
        try:
            periodo_raw = metadata_df.iloc[6, 0]
            # ✅ Convertir explícitamente a string
            periodo = str(periodo_raw).replace("PERIODO ", "").strip()

            tutor_name_raw = metadata_df.iloc[7, 0]
            # ✅ Convertir explícitamente a string
            tutor_full_name = str(tutor_name_raw).replace("DOCENTE ", "").strip()
        except (IndexError, AttributeError):
            raise HTTPException(status_code=400, detail="Error al leer la metadata del CSV. Formato inesperado.")

        # 3. BUSCAR AL TUTOR EN LA BD
        tutor = tutor_service.get_tutor_by_full_name_case_insensitive(db, tutor_full_name)
        if not tutor:
            raise HTTPException(status_code=404, detail=f"Tutor '{tutor_full_name}' no encontrado en la base de datos.")

        # 4. LEER LA TABLA DE ALUMNOS
        file_stream.seek(0)
        try:
            students_df = pd.read_csv(file_stream, skiprows=9, encoding='latin1', dtype={'NoControl': str})
        except pd.errors.EmptyDataError:
            return { "message": f"Archivo '{file.filename}' procesado. No se encontraron alumnos.", "nuevas_tutorias_creadas": 0, "alumnos_no_encontrados": 0 }
        except KeyError:
            raise HTTPException(status_code=400, detail="Columna 'NoControl' no encontrada en la tabla de alumnos del CSV.")

        # 5. ITERAR Y CREAR NUEVAS TUTORÍAS
        for index, row in students_df.iterrows():
            # Construir el número de fila real en el archivo original
            # ✅ Cast index to int before adding
            current_row_number = int(index) + 11 # +9 rows skipped + 1 for header + 1 for 0-based index #type: ignore

            # Validar que 'NoControl' no sea nulo/vacío antes de procesar
            if pd.isna(row['NoControl']) or not str(row['NoControl']).strip():
                errors.append(f"Fila {current_row_number}: Número de control vacío.")
                continue

            num_control = str(row['NoControl']).strip()

            # a. Buscar al alumno en la BD
            alumno = alumno_service.get_alumno_by_num_control(db, num_control)
            if not alumno:
                skipped_alumnos_not_found += 1
                errors.append(f"Fila {current_row_number}: Alumno con NoControl '{num_control}' no encontrado.")
                continue

            # b. Revisar si ya existe una tutoría para este alumno y periodo
            existing_tutoria: Optional[Tutoria] = db.exec( # Added type hint for clarity
                select(Tutoria).where(Tutoria.alumno_id == alumno.id_alumno, Tutoria.periodo == periodo)
            ).first()

            if existing_tutoria:
                errors.append(f"Fila {current_row_number}: Alumno '{num_control}' ya tiene tutoría para el periodo '{periodo}'.")
                continue

            # c. Crear el NUEVO registro de Tutoría
            # Ensure tutor.id_tutor is not None before assignment
            if tutor.id_tutor is None:
                errors.append(f"Error interno: ID del tutor '{tutor_full_name}' no encontrado después de la búsqueda.")
                continue # Should not happen if tutor object exists, but defensive check
            if alumno.id_alumno is None:
                errors.append(f"Error interno: ID del alumno '{num_control}' no encontrado después de la búsqueda.")
                continue # Should not happen

            nueva_tutoria = Tutoria(
                alumno_id=alumno.id_alumno,
                tutor_id=tutor.id_tutor,
                periodo=periodo,
                semestre=alumno.semestre_actual,
                estado=EstadoTutoria.PENDIENTE # O EN_CURSO
            )
            db.add(nueva_tutoria)
            processed_count += 1

        # 6. Guardar todos los cambios
        db.commit()

        # 7. Preparar la respuesta resumen
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
        print(f"ERROR INESPERADO procesando {file.filename}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error inesperado al procesar el archivo '{file.filename}'.")