# app/services/excel_generator_service.py

import io
from datetime import datetime
from typing import List, Dict, Any, Optional, Set # Añadido Set

# Importamos la librería de Excel
import openpyxl 
from openpyxl.styles import Alignment, Border, Side, Font 

# FastAPI / SQLModel
from sqlmodel import Session, select, func
from fastapi import HTTPException, status

# Models
from app.models.tutor import Tutor
from app.models.tutoria import Tutoria, EstadoTutoria
from app.models.alumno import Alumno
from app.models.reporte_integral import ReporteIntegral

# Ruta a la plantilla
TEMPLATE_ANEXO3_PATH = "app/excel_templates/ANEXO_3_formato.xlsx" 

def generate_anexo3_reporte(db: Session, periodo: str) -> io.BytesIO:
    """
    Genera el reporte "ANEXO 3" rellenando Hoja 2 (Detalle) y Hoja 1 (Resumen)
    con datos de la BD de forma dinámica.
    """
    
    # --- 1. Obtener Datos de la BD ---
    query = (
        select(Tutoria, Alumno, ReporteIntegral)
        .join(Alumno, Tutoria.alumno_id == Alumno.id_alumno) # type: ignore
        .outerjoin(ReporteIntegral, Tutoria.id_tutoria == ReporteIntegral.id_tutoria) # type: ignore
        .where(Tutoria.periodo == periodo)
        .order_by(Alumno.apellido_p, Alumno.apellido_m, Alumno.nombre) # type: ignore
    )
    resultados = db.exec(query).all()

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron tutorías asignadas para el periodo {periodo}."
        )

    # --- 2. Cargar la Plantilla de Excel ---
    try:
        workbook = openpyxl.load_workbook(TEMPLATE_ANEXO3_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"No se encontró la plantilla Excel en: {TEMPLATE_ANEXO3_PATH}")

    # --- 3. Definir Estilos Comunes ---
    thin_side = Side(style="thin", color="000000")
    all_borders = Border(left=thin_side, top=thin_side, right=thin_side, bottom=thin_side)
    bold_font = Font(bold=True)

    # ==========================================
    # === PROCESAMIENTO HOJA 2 (DETALLE) ===
    # ==========================================
    try:
        sheet2 = workbook["Hoja2"]
    except KeyError:
        raise HTTPException(status_code=500, detail="La plantilla no contiene una hoja llamada 'Hoja2'.")

    # Datos estáticos Hoja 2
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    sheet2["K14"] = fecha_actual

    # Lógica de Filas Dinámicas Hoja 2
    FILA_INICIO_H2 = 18
    fila_actual_h2 = FILA_INICIO_H2

    # --- Estructura para acumular datos del Resumen (Hoja 1) ---
    # Clave: (carrera, semestre)
    # Valor: Diccionario con contadores
    resumen_data: Dict[tuple, Dict[str, Any]] = {}

    for index, (tutoria, alumno, reporte) in enumerate(resultados):
        # --- A. Llenar Hoja 2 (Detalle) ---
        sheet2[f'A{fila_actual_h2}'] = f"{alumno.apellido_p} {alumno.apellido_m or ''} {alumno.nombre}".strip()
        sheet2[f'B{fila_actual_h2}'] = alumno.num_control
        sheet2[f'J{fila_actual_h2}'] = reporte.psicologia + reporte.ciencias_basicas + reporte.jefatura_academica
        
        # Variables auxiliares para el resumen
        r_grupal = 0
        r_individual = 0
        r_psicologia = 0
        r_ciencias = 0
        r_jefatura = 0

        if reporte:
            sheet2[f'C{fila_actual_h2}'] = reporte.tutoria_grupal
            sheet2[f'D{fila_actual_h2}'] = reporte.tutoria_individual
            sheet2[f'K{fila_actual_h2}'] = 1 if reporte.psicologia > 0 else 0
            sheet2[f'Q{fila_actual_h2}'] = 1 if reporte.ciencias_basicas > 0 else 0
            sheet2[f'R{fila_actual_h2}'] = 1 if reporte.jefatura_academica > 0 else 0
            
            # Valores para acumular
            r_grupal = reporte.tutoria_grupal
            r_individual = reporte.tutoria_individual
            r_psicologia = 1 if reporte.psicologia > 0 else 0
            r_ciencias = 1 if reporte.ciencias_basicas > 0 else 0
            r_jefatura = 1 if reporte.jefatura_academica > 0 else 0
        else:
            sheet2[f'C{fila_actual_h2}'] = 0
            sheet2[f'D{fila_actual_h2}'] = 0
            sheet2[f'K{fila_actual_h2}'] = ""
            sheet2[f'Q{fila_actual_h2}'] = ""
            sheet2[f'R{fila_actual_h2}'] = ""

        # Bordes Hoja 2
        for col_num in range(1, 19):
            cell = sheet2.cell(row=fila_actual_h2, column=col_num)
            cell.border = all_borders
        
        fila_actual_h2 += 1

        # --- B. Acumular Datos para Hoja 1 (Resumen) ---
        clave = (alumno.carrera, alumno.semestre_actual)
        
        if clave not in resumen_data:
            resumen_data[clave] = {
                "tutores_ids": set(), # Usamos un set para contar tutores únicos
                "total_grupal": 0,
                "total_individual": 0,
                "total_canalizaciones": 0
            }
        
        # Actualizar acumuladores
        resumen_data[clave]["tutores_ids"].add(tutoria.tutor_id)
        resumen_data[clave]["total_grupal"] += r_grupal
        resumen_data[clave]["total_individual"] += r_individual
        # Canalizaciones: Suma de las 3 áreas
        resumen_data[clave]["total_canalizaciones"] += (r_psicologia + r_ciencias + r_jefatura)


    # --- Totales Hoja 2 (Fórmulas) ---
    fila_total_h2 = fila_actual_h2
    fila_fin_datos_h2 = fila_actual_h2 - 1
    sheet2[f'A{fila_total_h2}'] = "TOTAL"
    sheet2.merge_cells(f'A{fila_total_h2}:B{fila_total_h2}')
    sheet2[f'C{fila_total_h2}'] = f"=SUM(C{FILA_INICIO_H2}:C{fila_fin_datos_h2})"
    sheet2[f'D{fila_total_h2}'] = f"=SUM(D{FILA_INICIO_H2}:D{fila_fin_datos_h2})"
    sheet2[f'J{fila_total_h2}'] = f"=SUM(J{FILA_INICIO_H2}:J{fila_fin_datos_h2})"
    sheet2[f'K{fila_total_h2}'] = f"=COUNTIF(K{FILA_INICIO_H2}:K{fila_fin_datos_h2}, \"1\")"
    sheet2[f'Q{fila_total_h2}'] = f"=COUNTIF(Q{FILA_INICIO_H2}:Q{fila_fin_datos_h2}, \"1\")"
    sheet2[f'R{fila_total_h2}'] = f"=COUNTIF(R{FILA_INICIO_H2}:R{fila_fin_datos_h2}, \"1\")"

    for col_num in range(1, 19):
        cell = sheet2.cell(row=fila_total_h2, column=col_num)
        cell.border = all_borders
        cell.font = bold_font
        cell.alignment = Alignment(horizontal="center", vertical="center")


    # ==========================================
    # === PROCESAMIENTO HOJA 1 (RESUMEN) ===
    # ==========================================
    try:
        sheet1 = workbook["Hoja1"]
    except KeyError:
        raise HTTPException(status_code=500, detail="La plantilla no contiene una hoja llamada 'Hoja1'.")

    FILA_INICIO_H1 = 18
    fila_actual_h1 = FILA_INICIO_H1
    
    # Ordenar las claves por Carrera y luego por Semestre para que se vea bonito
    claves_ordenadas = sorted(resumen_data.keys(), key=lambda x: (x[0], x[1]))

    for carrera, semestre in claves_ordenadas:
        datos = resumen_data[(carrera, semestre)]
        
        # Llenar Celdas
        sheet1[f'A{fila_actual_h1}'] = carrera
        sheet1[f'B{fila_actual_h1}'] = semestre
        sheet1[f'C{fila_actual_h1}'] = len(datos["tutores_ids"]) # Cuenta de tutores únicos
        sheet1[f'E{fila_actual_h1}'] = datos["total_grupal"]
        sheet1[f'F{fila_actual_h1}'] = datos["total_individual"]
        # Columna R: Canalizaciones al semestre (Suma total)
        sheet1[f'R{fila_actual_h1}'] = datos["total_canalizaciones"]

        # Aplicar bordes a la fila (Columnas A hasta R, o hasta donde llegue el formato)
        # Asumimos hasta la columna R (18) igual que la otra hoja
        for col_num in range(1, 28):
            cell = sheet1.cell(row=fila_actual_h1, column=col_num)
            cell.border = all_borders
            # Alinear centro para que se vea mejor (opcional)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_num == 1: # Alinear carrera a la izquierda
                cell.alignment = Alignment(horizontal="left", vertical="center")

        fila_actual_h1 += 1

    # --- Totales Hoja 1 (Fórmulas) ---
    fila_total_h1 = fila_actual_h1
    fila_fin_datos_h1 = fila_actual_h1 - 1
    
    sheet1[f'A{fila_total_h1}'] = "TOTAL"
    # Fusionar A y B para el título TOTAL
    sheet1.merge_cells(f'A{fila_total_h1}:B{fila_total_h1}') 
    
    # Fórmulas de suma para las columnas numéricas
    sheet1[f'C{fila_total_h1}'] = f"=SUM(C{FILA_INICIO_H1}:C{fila_fin_datos_h1})"
    sheet1[f'E{fila_total_h1}'] = f"=SUM(E{FILA_INICIO_H1}:E{fila_fin_datos_h1})"
    sheet1[f'F{fila_total_h1}'] = f"=SUM(F{FILA_INICIO_H1}:F{fila_fin_datos_h1})"
    sheet1[f'R{fila_total_h1}'] = f"=SUM(R{FILA_INICIO_H1}:R{fila_fin_datos_h1})"

    # Estilos Fila Total Hoja 1
    for col_num in range(1, 19):
        cell = sheet1.cell(row=fila_total_h1, column=col_num)
        cell.border = all_borders
        cell.font = bold_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # --- 8. Guardar el Excel en Memoria ---
    output_stream = io.BytesIO()
    workbook.save(output_stream)
    workbook.close()
    
    output_stream.seek(0)
    return output_stream

# --- FIN DEL ARCHIVO ---