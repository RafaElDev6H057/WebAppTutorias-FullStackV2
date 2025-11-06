"""
Servicio de generación de documentos PDF para el sistema de tutorías.

Proporciona funciones para generar PDFs de reportes integrales, constancias
de tutoría y reportes de proyectos (Reporte1), utilizando plantillas PDF base
y coordenadas predefinidas para posicionamiento de datos.
"""

import io
import copy
from typing import List, Dict, Any

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape, LETTER
from pypdf import PdfReader, PdfWriter

from sqlmodel import Session, select, func
from fastapi import HTTPException, status

from app.models.tutor import Tutor
from app.models.tutoria import Tutoria, EstadoTutoria
from app.models.alumno import Alumno
from app.models.reporte_integral import ReporteIntegral
from app.models.reporte1 import Reporte1
from app.services import reporte1_service

from app.core.pdf_coords.coords_pagina1 import coords as coords_p1, REF_W as P1_REF_W, REF_H as P1_REF_H
from app.core.pdf_coords.coords_pagina2 import coords as coords_p2, REF_W as P2_REF_W, REF_H as P2_REF_H
from app.core.pdf_coords.coords_constancia import coords_constancia, REF_W as CONST_REF_W, REF_H as CONST_REF_H
from app.core.pdf_coords.coords_reporte_g1 import coords as coords_r1, REF_W as R1_REF_W, REF_H as R1_REF_H

TEMPLATE_PDF_PATH = "app/pdf_templates/formato.pdf"
TEMPLATE_CONSTANCIA_PATH = "app/pdf_templates/formato_constancia.pdf"
TEMPLATE_REPORTE1_PATH = "app/pdf_templates/formato_reporte_g1_new.pdf"


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
    Crea un overlay PDF con datos renderizados en coordenadas específicas.
    
    Dibuja los datos de alumnos en un canvas transparente usando las coordenadas
    proporcionadas, escalando según las dimensiones de la página base.
    
    Args:
        data_to_draw: Lista de diccionarios con datos de alumnos a renderizar.
        coords_definition: Diccionario de coordenadas (x, y) para cada campo.
        is_first_page: Si es True, dibuja campos extra (tutor, periodo, etc.).
        base_page_width: Ancho de la página base en puntos.
        base_page_height: Alto de la página base en puntos.
        ref_width: Ancho de referencia usado al calcular coordenadas.
        ref_height: Alto de referencia usado al calcular coordenadas.
    
    Returns:
        PdfReader con el overlay generado.
    """
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


def generate_integral_report_pdf(db: Session, id_tutor: int, periodo: str) -> io.BytesIO:
    """
    Genera el PDF del Reporte Integral para un tutor y periodo específicos.
    
    Consulta la base de datos para obtener todas las tutorías del tutor en el periodo,
    combina los datos con los reportes integrales asociados, y genera un PDF multipágina
    con 11 alumnos en la primera página y 10 en las siguientes.
    
    Args:
        db: Sesión de base de datos.
        id_tutor: ID del tutor cuyos reportes se van a generar.
        periodo: Periodo académico (ej. "Enero-Junio 2025").
    
    Returns:
        Stream de bytes con el PDF generado.
    
    Raises:
        HTTPException: Si el tutor no existe, no hay tutorías para el periodo,
                    o hay error en la generación del PDF.
    """
    tutor = db.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tutor no encontrado."
        )
    
    tutor_full_name = f"{tutor.nombre} {tutor.apellido_p} {tutor.apellido_m or ''}".strip()
    
    query = (
        select(Tutoria, Alumno, ReporteIntegral)
        .join(Alumno, Tutoria.alumno_id == Alumno.id_alumno) #type: ignore
        .outerjoin(ReporteIntegral, Tutoria.id_tutoria == ReporteIntegral.id_tutoria) #type: ignore
        .where(Tutoria.tutor_id == id_tutor)
        .where(Tutoria.periodo == periodo)
        .order_by(Alumno.nombre, Alumno.apellido_p, Alumno.apellido_m) #type: ignore
    )
    
    results = db.exec(query).all()
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron tutorías para el tutor {id_tutor} en el periodo {periodo}."
        )
    
    alumnos_data_list: List[Dict[str, Any]] = []
    
    for tutoria, alumno, reporte in results:
        report_data = reporte if reporte else {}
        alumnos_data_list.append({
            "tutor": tutor_full_name,
            "departamento": "N/A",
            "periodo": periodo,
            "carrera": alumno.carrera,
            "nombre": f"{alumno.nombre} {alumno.apellido_p} {alumno.apellido_m or ''}".strip(),
            "grupal": getattr(report_data, 'tutoria_grupal', 0),
            "individual": getattr(report_data, 'tutoria_individual', 0),
            "seguimiento1": getattr(report_data, 'seguimiento_1', ''),
            "seguimiento2": getattr(report_data, 'seguimiento_2', ''),
            "seguimiento3": getattr(report_data, 'seguimiento_3', ''),
            "jefatura": getattr(report_data, 'jefatura_academica', 0),
            "ciencias": getattr(report_data, 'ciencias_basicas', 0),
            "psicologia": getattr(report_data, 'psicologia', 0),
            "aprobadas": getattr(report_data, 'materias_aprobadas', 0),
            "noaprobadas": getattr(report_data, 'materias_no_aprobadas', ''),
        })
    
    try:
        writer = PdfWriter()
        
        reader_p1 = PdfReader(TEMPLATE_PDF_PATH)
        if not reader_p1.pages:
            raise ValueError("Plantilla PDF vacía.")
        
        base_page_1 = copy.deepcopy(reader_p1.pages[0])
        base_w1 = float(base_page_1.mediabox.width)
        base_h1 = float(base_page_1.mediabox.height)
        
        alumnos_p1 = alumnos_data_list[:11]
        if alumnos_p1:
            overlay_reader_p1 = _draw_page_overlay(
                alumnos_p1, coords_p1, True, base_w1, base_h1, P1_REF_W, P1_REF_H
            )
            base_page_1.merge_page(overlay_reader_p1.pages[0])
        
        writer.add_page(base_page_1)
        
        alumnos_restantes = alumnos_data_list[11:]
        
        while alumnos_restantes:
            try:
                reader_loop = PdfReader(TEMPLATE_PDF_PATH)
                if len(reader_loop.pages) < 2:
                    break
                
                base_page_n = copy.deepcopy(reader_loop.pages[1])
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Error procesando plantilla PDF."
                )
            
            base_wn = float(base_page_n.mediabox.width)
            base_hn = float(base_page_n.mediabox.height)
            
            alumnos_pag = alumnos_restantes[:10]
            if not alumnos_pag:
                break
            
            overlay_reader_n = _draw_page_overlay(
                alumnos_pag, coords_p2, False, base_wn, base_hn, P2_REF_W, P2_REF_H
            )
            base_page_n.merge_page(overlay_reader_n.pages[0])
            writer.add_page(base_page_n)
            
            alumnos_restantes = alumnos_restantes[10:]
        
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        output_pdf_stream.seek(0)
        writer.close()
        
        return output_pdf_stream
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Plantilla PDF no encontrada: {TEMPLATE_PDF_PATH}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar PDF: {str(e)}"
        )


def generate_constancia_pdf(db: Session, id_alumno: int) -> io.BytesIO:
    """
    Genera el PDF de Constancia de Tutorías para un alumno específico.
    
    Verifica que el alumno haya completado al menos una tutoría antes de generar
    la constancia. El documento incluye el nombre completo del alumno en formato
    horizontal (landscape).
    
    Args:
        db: Sesión de base de datos.
        id_alumno: ID del alumno para quien se genera la constancia.
    
    Returns:
        Stream de bytes con el PDF generado.
    
    Raises:
        HTTPException: Si el alumno no existe, no tiene tutorías completadas,
                    o hay error en la generación del PDF.
    """
    alumno = db.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado."
        )
    
    query = select(func.count(Tutoria.id_tutoria)).where( #type:ignore
        Tutoria.alumno_id == id_alumno,
        Tutoria.estado == EstadoTutoria.COMPLETADA
    )
    
    tutorias_completadas = db.exec(query).one()
    
    if tutorias_completadas < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El alumno solo ha completado {tutorias_completadas} de 1 tutoría requerida."
        )
    
    nombre_completo = f"{alumno.nombre} {alumno.apellido_p} {alumno.apellido_m or ''}".strip().upper()
    data_to_draw = {"nombre_alumno": nombre_completo}
    
    try:
        reader = PdfReader(TEMPLATE_CONSTANCIA_PATH)
        writer = PdfWriter()
        
        base_page = reader.pages[0]
        base_w = float(base_page.mediabox.width)
        base_h = float(base_page.mediabox.height)
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(base_w, base_h))
        can.setFont("Helvetica-Bold", 12)
        
        scale_x = base_w / CONST_REF_W
        scale_y = base_h / CONST_REF_H
        
        coord = coords_constancia["nombre_alumno"]
        x = coord[0] * scale_x
        y = coord[1] * scale_y
        
        can.drawString(x, y, data_to_draw["nombre_alumno"])
        can.save()
        packet.seek(0)
        
        overlay_reader = PdfReader(packet)
        base_page.merge_page(overlay_reader.pages[0])
        writer.add_page(base_page)
        
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        writer.close()
        overlay_reader.stream.close()
        
        if hasattr(reader, 'stream') and not reader.stream.closed:
            reader.stream.close()
        
        output_pdf_stream.seek(0)
        return output_pdf_stream
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"No se encontró la plantilla de constancia: {TEMPLATE_CONSTANCIA_PATH}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ocurrió un error al generar la constancia: {str(e)}"
        )


def _dividir_texto_por_ancho(
    can: canvas.Canvas,
    texto: str,
    max_ancho: float,
    max_lineas: int
) -> List[str]:
    """
    Divide texto en líneas que caben dentro de un ancho máximo.
    
    Respeta saltos de línea manuales y divide por palabras para evitar
    cortes en medio de palabras.
    
    Args:
        can: Canvas de reportlab con fuente configurada.
        texto: Texto a dividir.
        max_ancho: Ancho máximo permitido en puntos.
        max_lineas: Número máximo de líneas a retornar.
    
    Returns:
        Lista de líneas de texto que caben en el ancho especificado.
    """
    lineas = []
    texto = texto or ""
    
    for linea in texto.split("\n"):
        palabras = linea.split(" ")
        linea_actual = ""
        
        for palabra in palabras:
            prueba = (linea_actual + " " + palabra).strip()
            
            if can.stringWidth(prueba, "Helvetica", 10) <= max_ancho:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
                
                if len(lineas) >= max_lineas:
                    return lineas[:max_lineas]
        
        if linea_actual:
            lineas.append(linea_actual)
            if len(lineas) >= max_lineas:
                return lineas[:max_lineas]
    
    return lineas[:max_lineas]


def _draw_multiline_text(
    can: canvas.Canvas,
    coord: tuple,
    texto: str,
    max_ancho_mm: float,
    max_lineas: int,
    line_height_mm: float = 4 * mm,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    line_height_scale: float = 1.0
):
    """
    Dibuja texto multilínea en coordenadas escaladas.
    
    Divide automáticamente el texto en líneas y lo renderiza de arriba
    hacia abajo, respetando el ancho máximo y el número de líneas permitido.
    
    Args:
        can: Canvas de reportlab.
        coord: Tupla (x, y) con coordenadas iniciales en milímetros.
        texto: Texto a dibujar.
        max_ancho_mm: Ancho máximo del texto en milímetros.
        max_lineas: Número máximo de líneas a dibujar.
        line_height_mm: Espaciado entre líneas en milímetros.
        scale_x: Factor de escala horizontal.
        scale_y: Factor de escala vertical.
        line_height_scale: Factor de escala para el espaciado de líneas.
    """
    x_start_mm, y_start_mm = coord
    x_start_pts = x_start_mm * scale_x
    y_start_pts = y_start_mm * scale_y
    line_height_pts = line_height_mm * line_height_scale
    max_ancho_pts = max_ancho_mm * scale_x
    
    lineas = _dividir_texto_por_ancho(can, texto, max_ancho_pts, max_lineas)
    
    y = y_start_pts
    for linea in lineas:
        can.drawString(x_start_pts, y, linea)
        y -= line_height_pts


def generate_reporte1_pdf(db: Session, reporte_id: int) -> io.BytesIO:
    """
    Genera el PDF del Reporte1 (Avance de Proyecto) para un reporte específico.
    
    Consulta los datos del reporte desde la base de datos y genera un PDF de una página
    con información detallada del proyecto incluyendo objetivos, metas, actividades,
    conclusiones y porcentaje de avance marcado visualmente.
    
    Args:
        db: Sesión de base de datos.
        reporte_id: ID del Reporte1 a generar.
    
    Returns:
        Stream de bytes con el PDF generado.
    
    Raises:
        HTTPException: Si el reporte no existe o hay error en la generación del PDF.
    """
    reporte = reporte1_service.get_reporte1_por_id(db, reporte_id)
    
    datos_pdf = {
        "profesor": reporte.nombre_tutor,
        "periodo": reporte.periodo,
        "proyecto": reporte.nombre_proyecto,
        "objetivo": reporte.objetivo,
        "descripcion": reporte.descripcion,
        "metas": reporte.metas,
        "actividades": reporte.actividades,
        "documentos": reporte.documentos_anexados or "",
        "conclusiones": reporte.conclusiones,
        "observaciones": reporte.observaciones,
        "firma_profesor": reporte.nombre_tutor,
        "firma_jefe": "",
    }
    
    try:
        reader = PdfReader(TEMPLATE_REPORTE1_PATH)
        writer = PdfWriter()
        
        base_page = reader.pages[0]
        base_w = float(base_page.mediabox.width)
        base_h = float(base_page.mediabox.height)
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(base_w, base_h))
        
        scale_x = base_w / R1_REF_W
        scale_y = base_h / R1_REF_H
        
        can.setFont("Helvetica", 10)
        
        campos_simples = ["profesor", "periodo", "proyecto", "firma_profesor", "firma_jefe"]
        for campo in campos_simples:
            if campo in coords_r1["campos"]:
                x_mm, y_mm = coords_r1["campos"][campo]
                texto = datos_pdf.get(campo, "")
                can.drawString(x_mm * scale_x, y_mm * scale_y, texto)
        
        line_height_mm = 4 * mm
        
        _draw_multiline_text(
            can, coords_r1["campos"]["objetivo"], datos_pdf["objetivo"],
            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["descripcion"], datos_pdf["descripcion"],
            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["metas"], datos_pdf["metas"],
            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["actividades"], datos_pdf["actividades"],
            max_ancho_mm=170*mm, max_lineas=6, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["documentos"], datos_pdf["documentos"],
            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["conclusiones"], datos_pdf["conclusiones"],
            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        _draw_multiline_text(
            can, coords_r1["campos"]["observaciones"], datos_pdf["observaciones"],
            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y
        )
        
        porcentaje_str = str(int(reporte.porcentaje_avance))
        if porcentaje_str in coords_r1["porcentajes"]:
            x_mm, y_mm = coords_r1["porcentajes"][porcentaje_str]
            can.setFont("Helvetica-Bold", 40)
            can.drawCentredString(x_mm * scale_x, y_mm * scale_y, "O")
        
        can.save()
        packet.seek(0)
        
        overlay_reader = PdfReader(packet)
        base_page.merge_page(overlay_reader.pages[0])
        writer.add_page(base_page)
        
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        writer.close()
        overlay_reader.stream.close()
        
        if hasattr(reader, 'stream') and not reader.stream.closed:
            reader.stream.close()
        
        output_pdf_stream.seek(0)
        return output_pdf_stream
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"No se encontró la plantilla de reporte: {TEMPLATE_REPORTE1_PATH}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ocurrió un error al generar el Reporte 1: {str(e)}"
        )
