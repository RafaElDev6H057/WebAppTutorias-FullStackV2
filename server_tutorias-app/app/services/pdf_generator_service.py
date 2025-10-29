# app/services/pdf_generator_service.py

import io
import copy
from typing import List, Dict, Any, Optional

# PDF Libraries
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape, LETTER
from pypdf import PdfReader, PdfWriter

# FastAPI / SQLModel
from sqlmodel import Session, select, func # Asegúrate de importar func
from fastapi import HTTPException, status

# Models
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria
from app.models.alumno import Alumno
from app.models.reporte_integral import ReporteIntegral

# Coordinate Files
from app.core.pdf_coords.coords_pagina1 import coords as coords_p1, REF_W as P1_REF_W, REF_H as P1_REF_H
from app.core.pdf_coords.coords_pagina2 import coords as coords_p2, REF_W as P2_REF_W, REF_H as P2_REF_H

# Path to template PDF
TEMPLATE_PDF_PATH = "app/pdf_templates/formato.pdf"

# --- Helper Function _draw_page_overlay (SIN CAMBIOS) ---
def _draw_page_overlay(
    data_to_draw: List[Dict[str, Any]],
    coords_definition: Dict[str, Any],
    is_first_page: bool,
    base_page_width: float,
    base_page_height: float,
    ref_width: float,
    ref_height: float
) -> PdfReader:
    # ... (código de _draw_page_overlay se mantiene igual) ...
    scale_x = base_page_width / ref_width
    scale_y = base_page_height / ref_height
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(base_page_width, base_page_height))
    can.setFont("Helvetica", 8)
    if is_first_page and "extra" in coords_definition and data_to_draw:
        extra_data = data_to_draw[0]
        for field_key, (x, y) in coords_definition["extra"].items():
            value = extra_data.get(field_key, '')
            can.drawString(x * scale_x, y * scale_y, str(value))
    num_alumnos_on_page = len(data_to_draw)
    max_slots_on_page = len(coords_definition.get("alumnos", []))
    for i in range(min(num_alumnos_on_page, max_slots_on_page)):
        alumno_data = data_to_draw[i]
        alumno_coords = coords_definition["alumnos"][i]
        for field_key, (x, y) in alumno_coords.items():
            value = alumno_data.get(field_key, '')
            if field_key in ["jefatura", "ciencias", "psicologia"]:
                display_value = "✔" if isinstance(value, int) and value > 0 else "✘"
            else:
                display_value = str(value)
            can.drawString(x * scale_x, y * scale_y, display_value)
    can.save()
    packet.seek(0)
    return PdfReader(packet)

# --- Main Service Function (CON BUCLE CORREGIDO) ---
def generate_integral_report_pdf(db: Session, id_tutor: int, periodo: str) -> io.BytesIO:
    """
    Genera el PDF del Reporte Integral para un Tutor y Periodo específicos.
    """
    # 1. Obtener datos del Tutor (sin cambios)
    tutor = db.get(Tutor, id_tutor)
    if not tutor: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor no encontrado.")
    tutor_full_name = f"{tutor.nombre} {tutor.apellido_p} {tutor.apellido_m or ''}".strip()

    # 2. Obtener Tutorías, Alumnos y Reportes (sin cambios)
    query = (
        select(Tutoria, Alumno, ReporteIntegral)
        .join(Alumno, Tutoria.alumno_id == Alumno.id_alumno) # type: ignore
        .outerjoin(ReporteIntegral, Tutoria.id_tutoria == ReporteIntegral.id_tutoria) # type: ignore
        .where(Tutoria.tutor_id == id_tutor)
        .where(Tutoria.periodo == periodo)
        .order_by(Alumno.apellido_p, Alumno.apellido_m, Alumno.nombre) # type: ignore
    )
    results = db.exec(query).all()
    if not results: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron tutorías para {id_tutor} en {periodo}.")

    # 3. Preparar lista de datos (sin cambios)
    alumnos_data_list: List[Dict[str, Any]] = []
    for tutoria, alumno, reporte in results:
        report_data = reporte if reporte else {}
        alumnos_data_list.append({
            "tutor": tutor_full_name, "departamento": "N/A", "periodo": periodo, "carrera": alumno.carrera,
            "nombre": f"{alumno.apellido_p} {alumno.apellido_m or ''} {alumno.nombre}".strip(),
            "grupal": getattr(report_data, 'tutoria_grupal', 0),
            "individual": getattr(report_data, 'tutoria_individual', 0),
            "seguimiento1": getattr(report_data, 'seguimiento_1', ''), "seguimiento2": getattr(report_data, 'seguimiento_2', ''), "seguimiento3": getattr(report_data, 'seguimiento_3', ''),
            "jefatura": getattr(report_data, 'jefatura_academica', 0), "ciencias": getattr(report_data, 'ciencias_basicas', 0), "psicologia": getattr(report_data, 'psicologia', 0),
            "aprobadas": getattr(report_data, 'materias_aprobadas', 0), "noaprobadas": getattr(report_data, 'materias_no_aprobadas', ''),
        })

    # 4. Generar el PDF
    try:
        writer = PdfWriter()

        # --- Página 1 ---
        # Leemos la plantilla una vez para la página 1
        reader_p1 = PdfReader(TEMPLATE_PDF_PATH)
        if not reader_p1.pages: raise ValueError("Plantilla PDF vacía.")
        base_page_1 = copy.deepcopy(reader_p1.pages[0])
        base_w1 = float(base_page_1.mediabox.width)
        base_h1 = float(base_page_1.mediabox.height)
        alumnos_p1 = alumnos_data_list[:11]
        if alumnos_p1:
            overlay_reader_p1 = _draw_page_overlay(alumnos_p1, coords_p1, True, base_w1, base_h1, P1_REF_W, P1_REF_H)
            base_page_1.merge_page(overlay_reader_p1.pages[0])
        writer.add_page(base_page_1)

        # --- Páginas Siguientes (BUCLE CORREGIDO) ---
        alumnos_restantes = alumnos_data_list[11:]
        page_number = 2

        while alumnos_restantes:
            print(f"DEBUG PDF Loop: Procesando página {page_number}. Alumnos restantes: {len(alumnos_restantes)}")

            # ✅ --- Volver a leer la plantilla para obtener una copia limpia de la pág 2 ---
            try:
                reader_loop = PdfReader(TEMPLATE_PDF_PATH)
                if len(reader_loop.pages) < 2:
                    # Si solo hay 1 página en la plantilla pero aún quedan alumnos
                    print(f"ADVERTENCIA: La plantilla solo tiene 1 página, pero quedan {len(alumnos_restantes)} alumnos. Se detiene la paginación.")
                    break # Salir del bucle si no hay pág 2
                base_page_n = copy.deepcopy(reader_loop.pages[1]) # Usamos deepcopy por seguridad
            except Exception as read_err:
                print(f"Error releyendo plantilla en bucle: {read_err}")
                raise HTTPException(status_code=500, detail="Error procesando plantilla PDF.")
            # --- Fin relectura ---

            base_wn = float(base_page_n.mediabox.width)
            base_hn = float(base_page_n.mediabox.height)

            alumnos_pag = alumnos_restantes[:10]
            if not alumnos_pag: break # Seguridad

            print(f"DEBUG PDF Loop: Alumnos para página {page_number}: {len(alumnos_pag)}")

            overlay_reader_n = _draw_page_overlay(
                alumnos_pag, coords_p2, False, base_wn, base_hn, P2_REF_W, P2_REF_H
            )
            base_page_n.merge_page(overlay_reader_n.pages[0])

            writer.add_page(base_page_n)

            alumnos_restantes = alumnos_restantes[10:]
            page_number += 1


        # 5. Guardar el PDF resultante en memoria
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        output_pdf_stream.seek(0)

        # Cerrar el PdfWriter
        writer.close()

        return output_pdf_stream

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Plantilla PDF no encontrada: {TEMPLATE_PDF_PATH}")
    except Exception as e:
        print(f"ERROR generando PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al generar PDF: {e}")