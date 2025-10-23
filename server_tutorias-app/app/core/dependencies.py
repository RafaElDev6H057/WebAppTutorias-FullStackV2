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

from app.models.tutor import Tutor
from app.schemas.tutor import TutorTokenData
# ❗ Import de tutor_service eliminado (no se usaba)

from app.core.config import SECRET_KEY, ALGORITHM

# --- Esquemas de Autenticación ---
oauth2_scheme_admin = OAuth2PasswordBearer(
    tokenUrl="/api/administradores/login",
    scheme_name="Admin_OAuth2"
)
oauth2_scheme_tutor = OAuth2PasswordBearer(
    tokenUrl="/api/tutores/login",
    scheme_name="Tutor_OAuth2"
)

# --- Dependencia para Administradores ---
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
        # ✅ Validación de tipo explícita (como en la función de tutor)
        usuario: Optional[str] = payload.get("sub")
        if usuario is None:
            raise credentials_exception
        # Ahora 'usuario' es un str garantizado
        token_data = TokenData(usuario=usuario)
    except JWTError:
        raise credentials_exception

    # ✅ Ya no se necesita #type:ignore
    user = admin_service.get_admin_by_usuario(db, usuario=token_data.usuario) #type: ignore
    if user is None:
        raise credentials_exception
    return user

# --- Dependencia para Tutores ---
def get_current_tutor_user(
    token: str = Depends(oauth2_scheme_tutor),
    db: Session = Depends(get_session)
) -> Tutor:
    """
    Dependencia para obtener el TUTOR actual a partir de un token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("\n--- DEBUG: Iniciando get_current_tutor_user ---") # DEBUG 1
    try:
        print(f"DEBUG DEPENDENCY: Secret key during validation: {SECRET_KEY}") # DEBUG 2
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG DEPENDENCY: Payload decodificado: {payload}") # DEBUG 3

        role: Optional[str] = payload.get("role")
        print(f"DEBUG DEPENDENCY: Rol obtenido: {role}") # DEBUG 4
        if role is None or role != "tutor":
            print("DEBUG DEPENDENCY: Fallo en validación de rol.") # DEBUG 5
            raise credentials_exception

        tutor_id: Optional[str] = payload.get("sub")
        print(f"DEBUG DEPENDENCY: ID (sub) obtenido: {tutor_id}") # DEBUG 6
        if tutor_id is None:
            print("DEBUG DEPENDENCY: Fallo, ID (sub) es None.") # DEBUG 7
            raise credentials_exception

        token_data = TutorTokenData(id=tutor_id, role=role)

    except JWTError as e:
        print(f"DEBUG DEPENDENCY: ¡JWTError! Error: {e}") # DEBUG 8
        raise credentials_exception

    if token_data.id is None:
        print("DEBUG DEPENDENCY: Fallo, token_data.id es None después de la creación.") # DEBUG 9
        raise credentials_exception
    try:
        tutor_pk = int(token_data.id)
        print(f"DEBUG DEPENDENCY: ID convertido a int: {tutor_pk}") # DEBUG 10
    except (ValueError, TypeError):
        print("DEBUG DEPENDENCY: Fallo al convertir ID a int.") # DEBUG 11
        raise credentials_exception

    print(f"DEBUG DEPENDENCY: Buscando tutor con ID {tutor_pk} en la BD...") # DEBUG 12
    user = db.get(Tutor, tutor_pk)

    if user is None:
        print("DEBUG DEPENDENCY: Fallo, tutor no encontrado en la BD.") # DEBUG 13
        raise credentials_exception
    print("--- DEBUG: get_current_tutor_user completado exitosamente ---") # DEBUG 14
    return user