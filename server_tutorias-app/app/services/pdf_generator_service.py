# app/services/pdf_generator_service.py

import io
import copy
from typing import List, Dict, Any, Optional

# PDF Libraries
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape, LETTER # Usamos landscape si el formato es horizontal
from pypdf import PdfReader, PdfWriter # Usamos pypdf (sucesor de PyPDF2)

# FastAPI / SQLModel
from sqlmodel import Session, select
from fastapi import HTTPException, status

# Models (Necesitamos Tutor, Tutoria, Alumno y ReporteIntegral)
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria
from app.models.alumno import Alumno
from app.models.reporte_integral import ReporteIntegral

# Coordinate Files (Ajusta la ruta si es necesario)
# Usamos las dimensiones de referencia definidas DENTRO de los archivos de coords
from app.core.pdf_coords.coords_pagina1 import coords as coords_p1, REF_W as P1_REF_W, REF_H as P1_REF_H
from app.core.pdf_coords.coords_pagina2 import coords as coords_p2, REF_W as P2_REF_W, REF_H as P2_REF_H

# Path to template PDF (Ajusta según tu estructura)
TEMPLATE_PDF_PATH = "app/pdf_templates/formato.pdf"

# --- Helper Function (Adaptada de tu script) ---
def _draw_page_overlay(
    data_to_draw: List[Dict[str, Any]],
    coords_definition: Dict[str, Any],
    is_first_page: bool,
    base_page_width: float,
    base_page_height: float,
    ref_width: float,
    ref_height: float
) -> PdfReader:
    """
    Crea UNA página PDF (overlay) en memoria con los datos proporcionados,
    usando las coordenadas definidas y escalándolas al tamaño de la página base.
    """
    # Calculamos factores de escala
    scale_x = base_page_width / ref_width
    scale_y = base_page_height / ref_height

    packet = io.BytesIO()
    # Usamos el tamaño de la página base de la plantilla para el canvas
    can = canvas.Canvas(packet, pagesize=(base_page_width, base_page_height))
    # TODO: Ajustar fuente y tamaño si es necesario
    can.setFont("Helvetica", 8) # Puede necesitar ajuste

    # --- Dibujar datos "extra" (solo en la primera página) ---
    if is_first_page and "extra" in coords_definition and data_to_draw:
        extra_data = data_to_draw[0] # Asumimos que los datos extra están en el primer dict
        for field_key, (x, y) in coords_definition["extra"].items():
            value = extra_data.get(field_key, '') # Obtenemos el valor o string vacío
            # Aplicamos escala a las coordenadas
            can.drawString(x * scale_x, y * scale_y, str(value))

    # --- Dibujar datos de alumnos ---
    num_alumnos_on_page = len(data_to_draw)
    max_slots_on_page = len(coords_definition.get("alumnos", []))

    for i in range(min(num_alumnos_on_page, max_slots_on_page)):
        alumno_data = data_to_draw[i]
        alumno_coords = coords_definition["alumnos"][i]
        for field_key, (x, y) in alumno_coords.items():
            value = alumno_data.get(field_key, '') # Obtenemos valor o vacío
            # Manejo especial para valores booleanos/numéricos que se representan con marcas
            if field_key in ["jefatura", "ciencias", "psicologia"]:
                 # Asume que 0 = No (✘), >0 = Sí (✔) - ¡AJUSTA SEGÚN TU LÓGICA DE BD!
                 display_value = "✔" if isinstance(value, int) and value > 0 else "✘"
            else:
                 display_value = str(value)

            # Aplicamos escala a las coordenadas
            can.drawString(x * scale_x, y * scale_y, display_value)

    can.save()
    packet.seek(0)
    # Devolvemos un PdfReader del overlay para facilitar la fusión
    return PdfReader(packet)

# --- Main Service Function ---
def generate_integral_report_pdf(db: Session, id_tutor: int, periodo: str) -> io.BytesIO:
    """
    Genera el PDF del Reporte Integral para un Tutor y Periodo específicos.
    """
    # 1. Obtener datos del Tutor
    tutor = db.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor no encontrado.")
    tutor_full_name = f"{tutor.nombre} {tutor.apellido_p} {tutor.apellido_m or ''}".strip()

    # 2. Obtener Tutorías, Alumnos y Reportes Integrales para ese Tutor y Periodo
    # Usamos LEFT JOIN para incluir tutorías aunque aún no tengan reporte
    query = (
        select(Tutoria, Alumno, ReporteIntegral)
        .join(Alumno, Tutoria.alumno_id == Alumno.id_alumno) #type:ignore
        .outerjoin(ReporteIntegral, Tutoria.id_tutoria == ReporteIntegral.id_tutoria) # LEFT JOIN #type:ignore
        .where(Tutoria.tutor_id == id_tutor)
        .where(Tutoria.periodo == periodo)
        # Opcional: Ordenar por nombre de alumno
        .order_by(Alumno.apellido_p, Alumno.apellido_m, Alumno.nombre) #type:ignore
    )
    results = db.exec(query).all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron tutorías asignadas para el tutor {id_tutor} en el periodo {periodo}."
        )

    # 3. Preparar la lista de diccionarios para la función de dibujo
    alumnos_data_list: List[Dict[str, Any]] = []
    for tutoria, alumno, reporte in results:
        report_data = reporte if reporte else {} # Usar dict vacío si no hay reporte
        alumno_dict = {
            # Datos extra (solo necesarios para el primer alumno, para la Pág 1)
            "tutor": tutor_full_name,
            "departamento": "N/A", # O obtenerlo de algún lado si es necesario
            "periodo": periodo,
            "carrera": alumno.carrera, # O la carrera asociada al grupo/tutoría si es diferente

            # Datos del Alumno y Reporte mapeados a las claves de coords_*.py
            "nombre": f"{alumno.apellido_p} {alumno.apellido_m or ''} {alumno.nombre}".strip(),
            "grupal": getattr(report_data, 'tutoria_grupal', 0), # Default 0 si no hay reporte
            "individual": getattr(report_data, 'tutoria_individual', 0),
            "seguimiento1": getattr(report_data, 'seguimiento_1', ''), # Default '' si no hay reporte
            "seguimiento2": getattr(report_data, 'seguimiento_2', ''),
            "seguimiento3": getattr(report_data, 'seguimiento_3', ''),
            "jefatura": getattr(report_data, 'jefatura_academica', 0),
            "ciencias": getattr(report_data, 'ciencias_basicas', 0),
            "psicologia": getattr(report_data, 'psicologia', 0),
            "aprobadas": getattr(report_data, 'materias_aprobadas', 0),
            "noaprobadas": getattr(report_data, 'materias_no_aprobadas', ''),
        }
        alumnos_data_list.append(alumno_dict)

    # 4. Generar el PDF usando la lógica adaptada de tu script
    try:
        reader = PdfReader(TEMPLATE_PDF_PATH)
        writer = PdfWriter()

        # --- Página 1 ---
        if not reader.pages:
            raise ValueError("El archivo de plantilla PDF está vacío o corrupto.")
        
        base_page_1 = copy.deepcopy(reader.pages[0])
        base_w1 = float(base_page_1.mediabox.width)
        base_h1 = float(base_page_1.mediabox.height)

        alumnos_p1 = alumnos_data_list[:11] # Primeros 11 alumnos
        if alumnos_p1: # Solo generar si hay datos
            overlay_reader_p1 = _draw_page_overlay(
                alumnos_p1, coords_p1, is_first_page=True,
                base_page_width=base_w1, base_page_height=base_h1,
                ref_width=P1_REF_W, ref_height=P1_REF_H
            )
            # Asumimos que no hay rotación por ahora, simplifica
            base_page_1.merge_page(overlay_reader_p1.pages[0])
        writer.add_page(base_page_1)

        # --- Páginas Siguientes ---
        alumnos_restantes = alumnos_data_list[11:]
        if len(reader.pages) < 2 and alumnos_restantes:
             raise ValueError("La plantilla necesita al menos 2 páginas si hay más de 11 alumnos.")

        while alumnos_restantes:
            if len(reader.pages) < 2: break # Seguridad extra

            base_page_n = copy.deepcopy(reader.pages[1]) # Usar siempre la Pág 2 de la plantilla
            base_wn = float(base_page_n.mediabox.width)
            base_hn = float(base_page_n.mediabox.height)

            alumnos_pag = alumnos_restantes[:10] # Siguientes 10 alumnos
            if not alumnos_pag: break # Seguridad extra

            overlay_reader_n = _draw_page_overlay(
                alumnos_pag, coords_p2, is_first_page=False,
                base_page_width=base_wn, base_page_height=base_hn,
                ref_width=P2_REF_W, ref_height=P2_REF_H
            )
            base_page_n.merge_page(overlay_reader_n.pages[0])
            writer.add_page(base_page_n)

            alumnos_restantes = alumnos_restantes[10:] # Actualizar restantes

        # 5. Guardar el PDF resultante en memoria
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        output_pdf_stream.seek(0) # Rebobinar el stream para leerlo después

        return output_pdf_stream

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"No se encontró el archivo de plantilla PDF en: {TEMPLATE_PDF_PATH}")
    except Exception as e:
        # Loggear el error real para depuración
        print(f"ERROR generando PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al generar el PDF: {e}")

# --- FIN DEL ARCHIVO ---