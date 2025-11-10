# clear_reports.py

import io
from sqlmodel import Session, select, update, delete
from fastapi import HTTPException
from typing import List

from app.database import engine
from app.models.tutoria import Tutoria
from app.models.reporte_integral import ReporteIntegral

def clear_integral_reports():
    print("--- Iniciando limpieza de Reportes Integrales y Banderas ---")
    
    with Session(engine) as session:
        try:
            # 1. Eliminar todos los registros de la tabla ReporteIntegral
            delete_statement = delete(ReporteIntegral)
            delete_result = session.exec(delete_statement) # type: ignore
            session.commit()
            
            print(f"✅ Reportes Integrales eliminados: {delete_result.rowcount}")

            # 2. Actualizar la bandera en TODAS las tutorías a False
            update_statement = (
                update(Tutoria)
                .where(Tutoria.reporte_integral_guardado == True) #type: ignore
                .values(reporte_integral_guardado=False)
            )
            update_result = session.exec(update_statement) # type: ignore
            session.commit()
            
            print(f"🚩 Banderas de Tutoría reiniciadas a 'False': {update_result.rowcount}")
            print("\n--- ¡Limpieza completada! ---")

        except Exception as e:
            print(f"🔴 ERROR durante la limpieza: {e}")
            session.rollback()

if __name__ == "__main__":
    # Importamos los modelos necesarios para que SQLAlchemy los reconozca
    from app.models.alumno import Alumno
    from app.models.tutor import Tutor
    
    print("ADVERTENCIA: Estás a punto de eliminar TODOS los reportes integrales")
    print("y reiniciar TODAS las banderas de 'reporte guardado' en las tutorías.")
    confirmacion = input("Escribe 'LIMPIAR' para confirmar: ")
    
    if confirmacion == "LIMPIAR":
        clear_integral_reports()
    else:
        print("Cancelado. No se han hecho cambios.")