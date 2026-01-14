"""
Coordenadas para posicionamiento de campos en el PDF de Constancia de Tutoría.

Define las posiciones exactas (en milímetros) donde se debe renderizar el nombre
del alumno en la constancia de tutoría, usando formato horizontal (landscape).
"""

from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.lib.units import mm

REF_W, REF_H = landscape(LETTER)
page_height = REF_H
page_width = REF_W

coords_constancia = {
    "nombre_alumno": (80 * mm, 146.3 * mm),
}
