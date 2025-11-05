"""
Configuración central de la aplicación.

Este módulo carga y expone las variables de configuración necesarias
para el funcionamiento de la aplicación, incluyendo credenciales de
seguridad y parámetros de autenticación JWT.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_por_defecto_deberia_ser_mas_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
