"""
Coordenadas para posicionamiento de campos en el PDF de Reporte General 1.

Define las posiciones exactas (en milímetros) donde se deben renderizar los campos
del reporte de proyecto de tutor, incluyendo coordenadas para marcar el porcentaje
de avance mediante círculos en escala de 10% a 100%.
"""

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import LETTER

REF_W, REF_H = LETTER

coords = {
    "campos": {
        "profesor": (68 * mm, 222.4 * mm),
        "periodo": (159 * mm, 222.4 * mm),
        "proyecto": (63.3 * mm, 217.6 * mm),
        "objetivo": (19.5 * mm, 185 * mm),
        "descripcion": (82 * mm, 185 * mm),
        "metas": (138.5 * mm, 185 * mm),
        "actividades": (20 * mm, 148.3 * mm),
        "documentos": (20 * mm, 120 * mm),
        "conclusiones": (20 * mm, 93 * mm),
        "observaciones": (20 * mm, 75 * mm),
        "firma_profesor": (25 * mm, 49 * mm),
        "firma_jefe": (102 * mm, 49 * mm),
    },
    "porcentajes": {
        "10": (27.6 * mm, 197 * mm),
        "20": (45.6 * mm, 197 * mm),
        "30": (63 * mm, 197 * mm),
        "40": (80.5 * mm, 197 * mm),
        "50": (98.5 * mm, 197 * mm),
        "60": (116 * mm, 197 * mm),
        "70": (134 * mm, 197 * mm),
        "80": (151 * mm, 197 * mm),
        "90": (169 * mm, 197 * mm),
        "100": (187 * mm, 197 * mm),
    }
}
