from reportlab.lib.units import mm
from reportlab.lib.pagesizes import LETTER

# Página 1: siempre se usa
REF_W, REF_H = LETTER

# Coordenadas base de ejemplo (ajusta según tu plantilla real)
coords = {
    "campos": {
        "profesor": (68 * mm, 222.4 * mm),
        "periodo": (170 * mm, 222.4 * mm),
        "proyecto": (60 * mm, 217.6 * mm),
        "objetivo": (19.5 * mm, 185 * mm),
        "descripcion": (82 * mm, 185 * mm),
        "metas": (138.5 * mm, 185 * mm),
        "actividades": (20 * mm, 150 * mm),
        "documentos": (20 * mm, 120 * mm),
        "conclusiones": (20 * mm, 93 * mm),
        "observaciones": (20 * mm, 75 * mm),
        "firma_profesor": (25 * mm, 49 * mm),
        "firma_jefe": (102 * mm, 49 * mm),
    },

    # Coordenadas para los círculos del porcentaje (10% al 100%)
    "porcentajes": {
        "10": (27.6 * mm, 201.5 * mm),
        "20": (45.6 * mm, 201.5 * mm),
        "30": (63 * mm, 201.5 * mm),
        "40": (80.5 * mm, 201.5 * mm),
        "50": (98.5 * mm, 201.5 * mm),
        "60": (116 * mm, 201.5 * mm),
        "70": (134 * mm, 201.5 * mm),
        "80": (151 * mm, 201.5 * mm),
        "90": (169 * mm, 201.5 * mm),
        "100": (187 * mm, 201.5 * mm),
    }
}
