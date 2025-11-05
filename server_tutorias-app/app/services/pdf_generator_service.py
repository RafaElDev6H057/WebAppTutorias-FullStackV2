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
from app.models.tutoria import Tutoria, EstadoTutoria
from app.models.alumno import Alumno
from app.models.reporte_integral import ReporteIntegral
from app.models.reporte1 import Reporte1

# --- Services ---
from app.services import reporte1_service

# Coordinate Files
from app.core.pdf_coords.coords_pagina1 import coords as coords_p1, REF_W as P1_REF_W, REF_H as P1_REF_H
from app.core.pdf_coords.coords_pagina2 import coords as coords_p2, REF_W as P2_REF_W, REF_H as P2_REF_H
from app.core.pdf_coords.coords_constancia import coords_constancia, REF_W as CONST_REF_W, REF_H as CONST_REF_H
from app.core.pdf_coords.coords_reporte_g1 import coords as coords_r1, REF_W as R1_REF_W, REF_H as R1_REF_H

# Path to template PDF
TEMPLATE_PDF_PATH = "app/pdf_templates/formato.pdf"
TEMPLATE_CONSTANCIA_PATH = "app/pdf_templates/formato_constancia.pdf"
TEMPLATE_REPORTE1_PATH = "app/pdf_templates/formato_reporte_g1.pdf"

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
        .order_by(Alumno.nombre, Alumno.apellido_p, Alumno.apellido_m) # type: ignore
    )
    results = db.exec(query).all()
    if not results: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron tutorías para {id_tutor} en {periodo}.")

    # 3. Preparar lista de datos (sin cambios)
    alumnos_data_list: List[Dict[str, Any]] = []
    for tutoria, alumno, reporte in results:
        report_data = reporte if reporte else {}
        alumnos_data_list.append({
            "tutor": tutor_full_name, "departamento": "N/A", "periodo": periodo, "carrera": alumno.carrera,
            "nombre": f"{alumno.nombre} {alumno.apellido_p} {alumno.apellido_m or ''}".strip(),
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
    
def generate_constancia_pdf(db: Session, id_alumno: int) -> io.BytesIO:
    """
    Genera el PDF de la Constancia de Tutorías para un alumno específico.
    """
    # ... (código para obtener alumno y verificar elegibilidad) ...
    alumno = db.get(Alumno, id_alumno)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado.")
    query = select(func.count(Tutoria.id_tutoria)).where( # type: ignore
        Tutoria.alumno_id == id_alumno,
        Tutoria.estado == EstadoTutoria.COMPLETADA
    )
    tutorias_completadas = db.exec(query).one()
    if tutorias_completadas < 1: # Mantenemos 1 para pruebas
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El alumno solo ha completado {tutorias_completadas} de 1 tutoría requerida."
        )

    # 3. Preparar los datos a dibujar
    nombre_completo = f"{alumno.nombre} {alumno.apellido_p} {alumno.apellido_m or ''}".strip().upper()
    data_to_draw = {
        "nombre_alumno": nombre_completo,
    }

    # 4. Generar el PDF
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

        # --- CAMBIO IMPORTANTE ---
        # Ahora usamos drawString (alineado a la izquierda) en lugar de drawCentredString
        
        # 1. Obtenemos las coordenadas
        coord = coords_constancia["nombre_alumno"]
        x = coord[0] * scale_x
        y = coord[1] * scale_y
        
        # 2. Ajustamos la coordenada X (la movemos más a la izquierda)
        # ya que ahora es el *inicio* del texto, no el *centro*.
        # Tienes que encontrar el 'x' correcto a prueba y error.
        # Probemos moviéndolo 60mm a la izquierda de tu coordenada centrada (136mm - 60mm = 76mm)
        
        # 👇 NUEVO CÁLCULO DE COORDENADA (Ajusta este 76mm)
        # x_alineado_izquierda = (76 * mm) * scale_x # ¡Este valor (76) necesitará ajuste!
        
        can.drawString(x, y, data_to_draw["nombre_alumno"])
        # --- FIN DEL CAMBIO ---

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
        raise HTTPException(status_code=500, detail=f"No se encontró la plantilla de constancia: {TEMPLATE_CONSTANCIA_PATH}")
    except Exception as e:
        print(f"ERROR generando constancia PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al generar la constancia: {e}")
    
# =========================================================
# === NUEVAS FUNCIONES AUXILIARES PARA REPORTE 1 (G1) ===
# =========================================================

def _dividir_texto_por_ancho(can: canvas.Canvas, texto: str, max_ancho: float, max_lineas: int) -> List[str]:
    """
    Divide el texto naturalmente según el ancho disponible (en puntos).
    Adaptado de tu script 'ya.py'.
    """
    lineas = []
    # Asegurarnos de que el texto no sea None
    texto = texto or ""
    for linea in texto.split("\n"):  # respeta saltos manuales
        palabras = linea.split(" ")
        linea_actual = ""
        for palabra in palabras:
            prueba = (linea_actual + " " + palabra).strip()
            # Asumimos la fuente y tamaño que usaremos
            # TODO: Pasar fontName y fontSize como argumentos si varían
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
    Dibuja texto multilínea en una coordenada escalada, dividiéndolo con la función auxiliar.
    """
    x_start_mm, y_start_mm = coord
    
    # Escalar las coordenadas y dimensiones
    x_start_pts = x_start_mm * scale_x
    y_start_pts = y_start_mm * scale_y
    line_height_pts = line_height_mm * line_height_scale # Usamos scale_y para la altura de línea
    max_ancho_pts = max_ancho_mm * scale_x # El ancho se escala con scale_x
    
    # Dividimos el texto
    lineas = _dividir_texto_por_ancho(can, texto, max_ancho_pts, max_lineas)
    
    # Dibujamos línea por línea, de arriba hacia abajo
    y = y_start_pts
    for linea in lineas:
        can.drawString(x_start_pts, y, linea)
        y -= line_height_pts # Moverse hacia abajo para la siguiente línea

# ==============================================
# === NUEVA FUNCIÓN PRINCIPAL PARA REPORTE 1 (G1) ===
# ==============================================

def generate_reporte1_pdf(db: Session, reporte_id: int) -> io.BytesIO:
    """
    Genera el PDF del Reporte 1 (Avance de Proyecto) para un reporte específico.
    """
    # 1. Obtener los datos del reporte desde la BD
    reporte = reporte1_service.get_reporte1_por_id(db, reporte_id)
    # get_reporte1_por_id ya lanza 404 si no se encuentra
    
    # 2. Preparar el diccionario de datos para el PDF
    # Mapeamos los nombres del modelo a los nombres de las coordenadas
    datos_pdf = {
        "profesor": reporte.nombre_tutor,
        "periodo": reporte.periodo,
        "proyecto": reporte.nombre_proyecto,
        "objetivo": reporte.objetivo,
        "descripcion": reporte.descripcion,
        "metas": reporte.metas,
        "actividades": reporte.actividades,
        "documentos": reporte.documentos_anexados or "", # Usar string vacío si es None
        "conclusiones": reporte.conclusiones,
        "observaciones": reporte.observaciones,
        "firma_profesor": reporte.nombre_tutor, # Usamos el nombre del tutor
        "firma_jefe": "", # Dejar vacío, o buscarlo si es necesario
    }

    # 3. Generar el PDF
    try:
        reader = PdfReader(TEMPLATE_REPORTE1_PATH)
        writer = PdfWriter()
        base_page = reader.pages[0] # Este reporte solo tiene 1 página
        
        base_w = float(base_page.mediabox.width)
        base_h = float(base_page.mediabox.height)
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(base_w, base_h))
        
        # Calculamos los factores de escala (las referencias vienen del archivo de coords)
        scale_x = base_w / R1_REF_W
        scale_y = base_h / R1_REF_H
        
        # --- Dibujar los datos en el lienzo ---
        
        # A. Definir fuentes y tamaños (¡ajustar según sea necesario!)
        can.setFont("Helvetica", 10) # Fuente por defecto
        
        # B. Dibujar campos de texto simples
        campos_simples = ["profesor", "periodo", "proyecto", "firma_profesor", "firma_jefe"]
        for campo in campos_simples:
            if campo in coords_r1["campos"]:
                x_mm, y_mm = coords_r1["campos"][campo]
                texto = datos_pdf.get(campo, "")
                can.drawString(x_mm * scale_x, y_mm * scale_y, texto)

        # C. Dibujar campos de texto multilínea
        # Ajusta los anchos (mm) y líneas máximas según tu plantilla
        line_height_mm = 4 * mm
        
        _draw_multiline_text(can, coords_r1["campos"]["objetivo"], datos_pdf["objetivo"], 
                            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm, 
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["descripcion"], datos_pdf["descripcion"], 
                            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["metas"], datos_pdf["metas"], 
                            max_ancho_mm=55*mm, max_lineas=10, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["actividades"], datos_pdf["actividades"], 
                            max_ancho_mm=170*mm, max_lineas=6, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["documentos"], datos_pdf["documentos"], 
                            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["conclusiones"], datos_pdf["conclusiones"], 
                            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)
        _draw_multiline_text(can, coords_r1["campos"]["observaciones"], datos_pdf["observaciones"], 
                            max_ancho_mm=170*mm, max_lineas=3, line_height_mm=line_height_mm,
                            scale_x=scale_x, scale_y=scale_y, line_height_scale=scale_y)

        # D. Dibujar la marca del porcentaje
        # Convertimos el float (ej. 70.0) a string "70"
        porcentaje_str = str(int(reporte.porcentaje_avance)) 
        if porcentaje_str in coords_r1["porcentajes"]:
            x_mm, y_mm = coords_r1["porcentajes"][porcentaje_str]
            can.setFont("Helvetica-Bold", 14) # Más grande para la marca
            can.drawCentredString(x_mm * scale_x, y_mm * scale_y, "✔")
        
        # Guardar el lienzo
        can.save()
        packet.seek(0)
        
        # Fusionar el overlay (lienzo) con la plantilla
        overlay_reader = PdfReader(packet)
        base_page.merge_page(overlay_reader.pages[0])
        writer.add_page(base_page)

        # 5. Guardar el PDF final en memoria
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        
        # Cerrar todos los streams
        writer.close()
        overlay_reader.stream.close()
        if hasattr(reader, 'stream') and not reader.stream.closed:
            reader.stream.close()
        
        output_pdf_stream.seek(0) # Rebobinar
        return output_pdf_stream

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"No se encontró la plantilla de reporte: {TEMPLATE_REPORTE1_PATH}")
    except Exception as e:
        print(f"ERROR generando Reporte 1 PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al generar el Reporte 1: {e}")