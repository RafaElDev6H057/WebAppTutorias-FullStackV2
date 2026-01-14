"""
Coordenadas para posicionamiento de campos en la página 2 del PDF de Reporte Integral.

Define las posiciones exactas (en milímetros) donde se deben renderizar los datos
de los alumnos en las páginas subsiguientes del reporte, usando tamaño carta vertical.
Soporta hasta 10 alumnos por página en páginas 2 y siguientes.
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm

REF_W, REF_H = LETTER
page_height = REF_H

seguimiento1_x = 91 * mm
seguimiento2_x = 108.5 * mm
seguimiento3_x = 125.5 * mm

coords = {
    "alumnos": [
        {
            "nombre": (10 * mm, page_height - 13 * mm),
            "grupal": (66 * mm, page_height - 12 * mm),
            "individual": (80 * mm, page_height - 12 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 7 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 7 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 7 * mm),
            "jefatura": (145 * mm, page_height - 11 * mm),
            "ciencias": (155 * mm, page_height - 11 * mm),
            "psicologia": (164 * mm, page_height - 11 * mm),
            "aprobadas": (180 * mm, page_height - 12 * mm),
            "noaprobadas": (192 * mm, page_height - 7 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 30 * mm),
            "grupal": (66 * mm, page_height - 30 * mm),
            "individual": (80 * mm, page_height - 30 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 25 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 25 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 25 * mm),
            "jefatura": (145 * mm, page_height - 29 * mm),
            "ciencias": (155 * mm, page_height - 29 * mm),
            "psicologia": (164 * mm, page_height - 29 * mm),
            "aprobadas": (180 * mm, page_height - 30 * mm),
            "noaprobadas": (192 * mm, page_height - 25 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 47 * mm),
            "grupal": (66 * mm, page_height - 47 * mm),
            "individual": (80 * mm, page_height - 47 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 42 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 42 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 42 * mm),
            "jefatura": (145 * mm, page_height - 46 * mm),
            "ciencias": (155 * mm, page_height - 46 * mm),
            "psicologia": (164 * mm, page_height - 46 * mm),
            "aprobadas": (180 * mm, page_height - 47 * mm),
            "noaprobadas": (192 * mm, page_height - 42 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 64 * mm),
            "grupal": (66 * mm, page_height - 64 * mm),
            "individual": (80 * mm, page_height - 64 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 59 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 59 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 59 * mm),
            "jefatura": (145 * mm, page_height - 63 * mm),
            "ciencias": (155 * mm, page_height - 63 * mm),
            "psicologia": (164 * mm, page_height - 63 * mm),
            "aprobadas": (180 * mm, page_height - 64 * mm),
            "noaprobadas": (192 * mm, page_height - 59 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 81 * mm),
            "grupal": (66 * mm, page_height - 81 * mm),
            "individual": (80 * mm, page_height - 81 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 76 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 76 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 76 * mm),
            "jefatura": (145 * mm, page_height - 80 * mm),
            "ciencias": (155 * mm, page_height - 80 * mm),
            "psicologia": (164 * mm, page_height - 80 * mm),
            "aprobadas": (180 * mm, page_height - 81 * mm),
            "noaprobadas": (192 * mm, page_height - 76 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 98 * mm),
            "grupal": (66 * mm, page_height - 98 * mm),
            "individual": (80 * mm, page_height - 98 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 93 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 93 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 93 * mm),
            "jefatura": (145 * mm, page_height - 97 * mm),
            "ciencias": (155 * mm, page_height - 97 * mm),
            "psicologia": (164 * mm, page_height - 97 * mm),
            "aprobadas": (180 * mm, page_height - 98 * mm),
            "noaprobadas": (192 * mm, page_height - 93 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 115 * mm),
            "grupal": (66 * mm, page_height - 115 * mm),
            "individual": (80 * mm, page_height - 115 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 110 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 110 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 110 * mm),
            "jefatura": (145 * mm, page_height - 114 * mm),
            "ciencias": (155 * mm, page_height - 114 * mm),
            "psicologia": (164 * mm, page_height - 114 * mm),
            "aprobadas": (180 * mm, page_height - 115 * mm),
            "noaprobadas": (192 * mm, page_height - 110 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 132 * mm),
            "grupal": (66 * mm, page_height - 132 * mm),
            "individual": (80 * mm, page_height - 132 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 127 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 127 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 127 * mm),
            "jefatura": (145 * mm, page_height - 131 * mm),
            "ciencias": (155 * mm, page_height - 131 * mm),
            "psicologia": (164 * mm, page_height - 131 * mm),
            "aprobadas": (180 * mm, page_height - 132 * mm),
            "noaprobadas": (192 * mm, page_height - 127 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 149 * mm),
            "grupal": (66 * mm, page_height - 149 * mm),
            "individual": (80 * mm, page_height - 149 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 144 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 144 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 144 * mm),
            "jefatura": (145 * mm, page_height - 148 * mm),
            "ciencias": (155 * mm, page_height - 148 * mm),
            "psicologia": (164 * mm, page_height - 148 * mm),
            "aprobadas": (180 * mm, page_height - 149 * mm),
            "noaprobadas": (192 * mm, page_height - 144 * mm),
        },
        {
            "nombre": (10 * mm, page_height - 166 * mm),
            "grupal": (66 * mm, page_height - 166 * mm),
            "individual": (80 * mm, page_height - 166 * mm),
            "seguimiento1": (seguimiento1_x, page_height - 161 * mm),
            "seguimiento2": (seguimiento2_x, page_height - 161 * mm),
            "seguimiento3": (seguimiento3_x, page_height - 161 * mm),
            "jefatura": (145 * mm, page_height - 165 * mm),
            "ciencias": (155 * mm, page_height - 165 * mm),
            "psicologia": (164 * mm, page_height - 165 * mm),
            "aprobadas": (180 * mm, page_height - 166 * mm),
            "noaprobadas": (192 * mm, page_height - 161 * mm),
        },
    ]
}
