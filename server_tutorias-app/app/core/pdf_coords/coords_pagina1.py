# app/core/pdf_coords/coords_pagina1.py

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm

# Define las dimensiones de referencia usadas para calcular estas coordenadas
# (Asumimos que se basaron en tamaño CARTA vertical)
REF_W, REF_H = LETTER
page_height = REF_H # Usamos un alias más corto para las coordenadas

coords = {
    "extra": {
        "tutor": (26*mm, page_height - 38*mm),
        "departamento": (33*mm, page_height - 44*mm), # ¿Necesitamos este dato?
        "periodo": (128*mm, page_height - 38*mm),
        "carrera": (120*mm, page_height - 44*mm), # ¿Necesitamos este dato?
    },
    "alumnos": [
            # Cada alumno es un dict de coordenadas
            #ALUMNO 1
            {
                "nombre": (10*mm, page_height - 74*mm),
                "grupal": (66*mm, page_height - 74*mm),
                "individual": (80*mm, page_height - 74*mm),
                "seguimiento1": (90*mm, page_height - 69*mm),
                "seguimiento2": (107.5*mm, page_height - 69*mm),
                "seguimiento3": (124.5*mm, page_height - 69*mm),
                "jefatura": (145*mm, page_height - 73*mm),
                "ciencias": (155*mm, page_height - 73*mm),
                "psicologia": (164*mm, page_height - 73*mm),
                "aprobadas": (180*mm, page_height - 74*mm),
                "noaprobadas": (192*mm, page_height - 69*mm),
            },
            # ALUMNO 2
            {
                "nombre": (10*mm, page_height - 91*mm),
                "grupal": (66*mm, page_height - 91*mm),
                "individual": (80*mm, page_height - 91*mm),
                "seguimiento1": (90*mm, page_height - 86*mm),
                "seguimiento2": (107.5*mm, page_height - 86*mm),
                "seguimiento3": (124.5*mm, page_height - 86*mm),
                "jefatura": (145*mm, page_height - 90*mm),
                "ciencias": (155*mm, page_height - 90*mm),
                "psicologia": (164*mm, page_height - 90*mm),
                "aprobadas": (180*mm, page_height - 91*mm),
                "noaprobadas": (192*mm, page_height - 86*mm),
            },
            # ALUMNO 3
            {
                "nombre": (10*mm, page_height - 109*mm),
                "grupal": (66*mm, page_height - 109*mm),
                "individual": (80*mm, page_height - 109*mm),
                "seguimiento1": (90*mm, page_height - 104*mm),
                "seguimiento2": (107.5*mm, page_height - 104*mm),
                "seguimiento3": (124.5*mm, page_height - 104*mm),
                "jefatura": (145*mm, page_height - 108*mm),
                "ciencias": (155*mm, page_height - 108*mm),
                "psicologia": (164*mm, page_height - 108*mm),
                "aprobadas": (180*mm, page_height - 109*mm),
                "noaprobadas": (192*mm, page_height - 104*mm),
            },
            # ALUMNO 4
            {
                "nombre": (10*mm, page_height - 126*mm),
                "grupal": (66*mm, page_height - 126*mm),
                "individual": (80*mm, page_height - 126*mm),
                "seguimiento1": (90*mm, page_height - 121*mm),
                "seguimiento2": (107.5*mm, page_height - 121*mm),
                "seguimiento3": (124.5*mm, page_height - 121*mm),
                "jefatura": (145*mm, page_height - 125*mm),
                "ciencias": (155*mm, page_height - 125*mm),
                "psicologia": (164*mm, page_height - 125*mm),
                "aprobadas": (180*mm, page_height - 126*mm),
                "noaprobadas": (192*mm, page_height - 121*mm),
            },
            # ALUMNO 5
            {
                "nombre": (10*mm, page_height - 143*mm),
                "grupal": (66*mm, page_height - 143*mm),
                "individual": (80*mm, page_height - 143*mm),
                "seguimiento1": (90*mm, page_height - 138*mm),
                "seguimiento2": (107.5*mm, page_height - 138*mm),
                "seguimiento3": (124.5*mm, page_height - 138*mm),
                "jefatura": (145*mm, page_height - 142*mm),
                "ciencias": (155*mm, page_height - 142*mm),
                "psicologia": (164*mm, page_height - 142*mm),
                "aprobadas": (180*mm, page_height - 143*mm),
                "noaprobadas": (192*mm, page_height - 138*mm),
            },
            # ALUMNO 6
            {
                "nombre": (10*mm, page_height - 160*mm),
                "grupal": (66*mm, page_height - 160*mm),
                "individual": (80*mm, page_height - 160*mm),
                "seguimiento1": (90*mm, page_height - 155*mm),
                "seguimiento2": (107.5*mm, page_height - 155*mm),
                "seguimiento3": (124.5*mm, page_height - 155*mm),
                "jefatura": (145*mm, page_height - 159*mm),
                "ciencias": (155*mm, page_height - 159*mm),
                "psicologia": (164*mm, page_height - 159*mm),
                "aprobadas": (180*mm, page_height - 160*mm),
                "noaprobadas": (192*mm, page_height - 155*mm),
            },
            # ALUMNO 7
            {
                "nombre": (10*mm, page_height - 177*mm),
                "grupal": (66*mm, page_height - 177*mm),
                "individual": (80*mm, page_height - 177*mm),
                "seguimiento1": (90*mm, page_height - 172*mm),
                "seguimiento2": (107.5*mm, page_height - 172*mm),
                "seguimiento3": (124.5*mm, page_height - 172*mm),
                "jefatura": (145*mm, page_height - 176*mm),
                "ciencias": (155*mm, page_height - 176*mm),
                "psicologia": (164*mm, page_height - 176*mm),
                "aprobadas": (180*mm, page_height - 177*mm),
                "noaprobadas": (192*mm, page_height - 172*mm),
            },
            # ALUMNO 8
            {
                "nombre": (10*mm, page_height - 195*mm),
                "grupal": (66*mm, page_height - 195*mm),
                "individual": (80*mm, page_height - 195*mm),
                "seguimiento1": (90*mm, page_height - 190*mm),
                "seguimiento2": (107.5*mm, page_height - 190*mm),
                "seguimiento3": (124.5*mm, page_height - 190*mm),
                "jefatura": (145*mm, page_height - 194*mm),
                "ciencias": (155*mm, page_height - 194*mm),
                "psicologia": (164*mm, page_height - 194*mm),
                "aprobadas": (180*mm, page_height - 195*mm),
                "noaprobadas": (192*mm, page_height - 190*mm),
            },
            # ALUMNO 9
            {
                "nombre": (10*mm, page_height - 212*mm),
                "grupal": (66*mm, page_height - 212*mm),
                "individual": (80*mm, page_height - 212*mm),
                "seguimiento1": (90*mm, page_height - 207*mm),
                "seguimiento2": (107.5*mm, page_height - 207*mm),
                "seguimiento3": (124.5*mm, page_height - 207*mm),
                "jefatura": (145*mm, page_height - 211*mm),
                "ciencias": (155*mm, page_height - 211*mm),
                "psicologia": (164*mm, page_height - 211*mm),
                "aprobadas": (180*mm, page_height - 212*mm),
                "noaprobadas": (192*mm, page_height - 207*mm),
            },
            # ALUMNO 10
            {
                "nombre": (10*mm, page_height - 229*mm),
                "grupal": (66*mm, page_height - 229*mm),
                "individual": (80*mm, page_height - 229*mm),
                "seguimiento1": (90*mm, page_height - 224*mm),
                "seguimiento2": (107.5*mm, page_height - 224*mm),
                "seguimiento3": (124.5*mm, page_height - 224*mm),
                "jefatura": (145*mm, page_height - 228*mm),
                "ciencias": (155*mm, page_height - 228*mm),
                "psicologia": (164*mm, page_height - 228*mm),
                "aprobadas": (180*mm, page_height - 229*mm),
                "noaprobadas": (192*mm, page_height - 224*mm),
            },
            # ALUMNO 11
            {
                "nombre": (10*mm, page_height - 246*mm),
                "grupal": (66*mm, page_height - 246*mm),
                "individual": (80*mm, page_height - 246*mm),
                "seguimiento1": (90*mm, page_height - 241*mm),
                "seguimiento2": (107.5*mm, page_height - 241*mm),
                "seguimiento3": (124.5*mm, page_height - 241*mm),
                "jefatura": (145*mm, page_height - 245*mm),
                "ciencias": (155*mm, page_height - 245*mm),
                "psicologia": (164*mm, page_height - 245*mm),
                "aprobadas": (180*mm, page_height - 246*mm),
                "noaprobadas": (192*mm, page_height - 241*mm),
            },
            
        ]
}