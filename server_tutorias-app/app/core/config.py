# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Para generar una clave secreta segura, puedes usar: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_por_defecto_deberia_ser_mas_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30