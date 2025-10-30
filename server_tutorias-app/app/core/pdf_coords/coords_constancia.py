# app/core/pdf_coords/coords_constancia.py

from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.lib.units import mm

# --- Dimensiones de Referencia ---
# Usamos landscape(LETTER) porque tu formato es horizontal (apaisado)
REF_W, REF_H = landscape(LETTER)
page_height = REF_H
page_width = REF_W

# --- Coordenadas (X, Y) para la Constancia ---
# (0, 0) es la esquina inferior izquierda de la página.

# NOTA: ¡Estos valores son una SUPOSICIÓN INICIAL y necesitarán ajuste!
coords_constancia = {
    
    # "Se le reconoce al alumno:" está aprox. a 60mm de la izquierda y 115mm de abajo.
    # El nombre debería ir justo debajo o al lado de eso.
    # Probemos con 70mm desde la izquierda y 105mm desde abajo.
    "nombre_alumno": (136 * mm, 146.3 * mm),
    
    # Dejamos un placeholder para la fecha, como pediste
    # "fecha_expedicion": (70 * mm, 80 * mm),
}