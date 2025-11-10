# populate_fake_reports.py

import io
import random # 👈 1. Importamos el módulo random
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List

from app.database import engine
from app.models.tutoria import Tutoria
from app.models.reporte_integral import ReporteIntegral
from app.schemas.reporte_integral import ReporteIntegralCreate

# --- CONFIGURACIÓN ---
PERIODO_A_RELLENAR = "22025" 

# 2. Definimos solo los datos FALSOS que serán ESTÁTICOS
STATIC_FAKE_DATA = {
    "seguimiento_1": "OK",
    "seguimiento_2": "OK",
    "seguimiento_3": "OK",
    "materias_no_aprobadas": "Ninguna",
}
# ---------------------

def populate_reports_for_period(periodo: str):
    print(f"--- Iniciando generación de reportes FALSOS y ALEATORIOS para el periodo: {periodo} ---")
    
    reportes_creados = 0
    reportes_actualizados = 0
    tutorias_actualizadas = 0

    with Session(engine) as session:
        # 1. Buscar todas las tutorías del periodo
        query_tutorias = select(Tutoria).where(Tutoria.periodo == periodo)
        tutorias_del_periodo: List[Tutoria] = session.exec(query_tutorias).all() #type: ignore

        if not tutorias_del_periodo:
            print(f"❌ Error: No se encontraron tutorías para el periodo {periodo}.")
            return

        print(f"Encontradas {len(tutorias_del_periodo)} tutorías para procesar...")

        for tutoria in tutorias_del_periodo:
            # 2. Revisar si ya existe un reporte
            existing_report = session.exec(
                select(ReporteIntegral).where(ReporteIntegral.id_tutoria == tutoria.id_tutoria)
            ).first()
            
            # 3. 👇 Generamos los datos aleatorios DENTRO del bucle
            dynamic_fake_data = {
                "tutoria_grupal": random.randint(1, 16),
                "tutoria_individual": random.randint(1, 5),
                "jefatura_academica": random.randint(0, 1),
                "ciencias_basicas": random.randint(0, 1),
                "psicologia": random.randint(0, 1),
                "materias_aprobadas": random.randint(6, 8),
            }

            # 4. Combinamos los datos para crear el payload
            reporte_data = ReporteIntegralCreate(
                **STATIC_FAKE_DATA,    # Los campos estáticos #type: ignore
                **dynamic_fake_data,   # Los campos aleatorios
                id_tutoria=tutoria.id_tutoria # El ID de la tutoría #type: ignore
            )
            
            if existing_report:
                # Si ya existe, lo actualizamos
                update_data = reporte_data.model_dump(exclude={"id_tutoria"})
                for key, value in update_data.items():
                    setattr(existing_report, key, value)
                session.add(existing_report)
                reportes_actualizados += 1
            else:
                # Si no existe, creamos uno nuevo
                new_report = ReporteIntegral.model_validate(reporte_data)
                session.add(new_report)
                reportes_creados += 1
            
            # 5. Actualizamos la bandera de la tutoría
            if not tutoria.reporte_integral_guardado:
                tutoria.reporte_integral_guardado = True
                session.add(tutoria)
                tutorias_actualizadas += 1

        # 6. Guardar todos los cambios
        try:
            session.commit()
            print("\n--- ¡Proceso completado! ---")
            print(f"✅ Reportes Integrales creados: {reportes_creados}")
            print(f"🔄 Reportes Integrales actualizados: {reportes_actualizados}")
            print(f"🚩 Banderas de Tutoría actualizadas a 'True': {tutorias_actualizadas}")

        except Exception as e:
            print(f"🔴 ERROR al guardar los cambios en la BD: {e}")
            session.rollback()

if __name__ == "__main__":
    # Importamos los modelos necesarios para que SQLAlchemy los reconozca
    from app.models.alumno import Alumno
    from app.models.tutor import Tutor
    
    populate_reports_for_period(PERIODO_A_RELLENAR)