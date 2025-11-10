# app/services/excel_generator_service.py

import io
from datetime import datetime
from typing import List, Dict, Any, Optional

# Importamos la librería de Excel
import openpyxl 
# Importamos estilos de celda
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
    Genera el reporte "ANEXO 3" rellenando la Hoja 2 con datos de la BD
    de forma dinámica, y añadiendo FÓRMULAS de totales al final.
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

    # --- 3. Trabajar con la Hoja 2 ---
    try:
        sheet = workbook["Hoja2"]
    except KeyError:
        raise HTTPException(status_code=500, detail="La plantilla no contiene una hoja llamada 'Hoja2'.")

    # --- 4. Rellenar Datos Estáticos (Fecha) ---
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    sheet["K14"] = fecha_actual

    # --- 5. Definir Estilos (Bordes y Fuentes) ---
    thin_side = Side(style="thin", color="000000")
    all_borders = Border(left=thin_side, top=thin_side, right=thin_side, bottom=thin_side)
    bold_font = Font(bold=True)
    
    # --- 6. Rellenar Datos de Alumnos ---
    FILA_INICIO_ALUMNOS = 18
    fila_actual = FILA_INICIO_ALUMNOS # Empezamos en la fila 18
    
    # ❗ Ya NO necesitamos contadores de Python

    for index, (tutoria, alumno, reporte) in enumerate(resultados):
        
        # Mapeo de datos (siempre existen)
        sheet[f'A{fila_actual}'] = f"{alumno.apellido_p} {alumno.apellido_m or ''} {alumno.nombre}".strip()
        sheet[f'B{fila_actual}'] = alumno.num_control
        sheet[f'J{fila_actual}'] = 1 # Valor fijo
        
        if reporte:
            sheet[f'C{fila_actual}'] = reporte.tutoria_grupal
            sheet[f'D{fila_actual}'] = reporte.tutoria_individual
            sheet[f'K{fila_actual}'] = "X" if reporte.psicologia > 0 else ""
            sheet[f'Q{fila_actual}'] = "X" if reporte.ciencias_basicas > 0 else ""
            sheet[f'R{fila_actual}'] = "X" if reporte.jefatura_academica > 0 else ""
        else:
            sheet[f'C{fila_actual}'] = 0
            sheet[f'D{fila_actual}'] = 0
            sheet[f'K{fila_actual}'] = ""
            sheet[f'Q{fila_actual}'] = ""
            sheet[f'R{fila_actual}'] = ""

        # Aplicar bordes a la fila (Columnas A hasta R)
        for col_num in range(1, 19):
            cell = sheet.cell(row=fila_actual, column=col_num)
            cell.border = all_borders
        
        fila_actual += 1 # Incrementar el contador de fila

    # --- 7. Añadir Fila de Totales (CON FÓRMULAS) ---
    # 'fila_actual' ahora apunta a la primera fila vacía (ej. Fila 46 si hay 28 alumnos)
    # 'fila_fin_datos' es la fila anterior (ej. Fila 45)
    fila_total = fila_actual
    fila_fin_datos = fila_actual - 1

    sheet[f'A{fila_total}'] = "TOTAL"
    sheet.merge_cells(f'A{fila_total}:B{fila_total}') # Combinar celdas

    # ✅ Escribimos las fórmulas de Excel
    # Nota: openpyxl usa las fórmulas en INGLÉS (SUM, COUNTIF)
    sheet[f'C{fila_total}'] = f"=SUM(C{FILA_INICIO_ALUMNOS}:C{fila_fin_datos})"
    sheet[f'D{fila_total}'] = f"=SUM(D{FILA_INICIO_ALUMNOS}:D{fila_fin_datos})"
    sheet[f'J{fila_total}'] = f"=SUM(J{FILA_INICIO_ALUMNOS}:J{fila_fin_datos})"
    sheet[f'K{fila_total}'] = f"=COUNTIF(K{FILA_INICIO_ALUMNOS}:K{fila_fin_datos}, \"X\")"
    sheet[f'Q{fila_total}'] = f"=COUNTIF(Q{FILA_INICIO_ALUMNOS}:Q{fila_fin_datos}, \"X\")"
    sheet[f'R{fila_total}'] = f"=COUNTIF(R{FILA_INICIO_ALUMNOS}:R{fila_fin_datos}, \"X\")"

    # Aplicar estilos a la fila de totales
    for col_num in range(1, 19):
        cell = sheet.cell(row=fila_total, column=col_num)
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