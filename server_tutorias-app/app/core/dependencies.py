# app/core/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import JWTError, jwt
from typing import Optional

from app.database import get_session
from app.models.administrador import Administrador
from app.schemas.administrador import TokenData
from app.services import admin_service
from app.core.config import SECRET_KEY, ALGORITHM

# 1. Definimos el esquema de autenticación para Administradores
# Apunta a la URL de login del administrador
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/api/administradores/login")

def get_current_admin_user(
    token: str = Depends(oauth2_scheme_admin), 
    db: Session = Depends(get_session)
) -> Administrador:
    """
    Dependencia para obtener el administrador actual a partir de un token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: Optional[str] = payload.get("sub")
        if usuario is None:
            raise credentials_exception
        token_data = TokenData(usuario=usuario)
    except JWTError:
        raise credentials_exception
    
    user = admin_service.get_admin_by_usuario(db, usuario=token_data.usuario) #type: ignore
    if user is None:
        raise credentials_exception
    return user