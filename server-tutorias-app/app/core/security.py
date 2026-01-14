"""
Utilidades de seguridad y criptografía.

Proporciona funciones para el hashing de contraseñas y generación
de tokens JWT para autenticación de usuarios.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que una contraseña en texto plano coincida con su hash.
    
    Args:
        plain_password: Contraseña en texto plano a verificar.
        hashed_password: Hash bcrypt de la contraseña almacenada.
    
    Returns:
        True si la contraseña es válida, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash bcrypt de una contraseña en texto plano.
    
    Args:
        password: Contraseña en texto plano a hashear.
    
    Returns:
        Hash bcrypt de la contraseña.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado con los datos proporcionados.
    
    Args:
        data: Diccionario con los datos a incluir en el payload del token.
        expires_delta: Tiempo de expiración personalizado. Si no se especifica,
        el token expirará en 15 minutos.
    
    Returns:
        Token JWT codificado como string.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt
