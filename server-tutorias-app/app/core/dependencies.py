"""
Dependencias de inyección para autenticación y autorización.

Proporciona funciones de dependencia para FastAPI que validan tokens JWT
y obtienen el usuario autenticado actual según su rol (administrador, tutor o alumno).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import JWTError, jwt
from typing import Optional, Union

from app.database import get_session
from app.models.administrador import Administrador, RolAdministrador # Importamos el Enum de Roles
from app.models.tutor import Tutor
from app.models.alumno import Alumno
from app.schemas.administrador import TokenData
from app.schemas.tutor import TutorTokenData
from app.schemas.alumno import AlumnoTokenData
from app.services import admin_service
from app.core.config import settings


oauth2_scheme_admin = OAuth2PasswordBearer(
    tokenUrl="/api/administradores/login",
    scheme_name="Admin_OAuth2"
)

oauth2_scheme_tutor = OAuth2PasswordBearer(
    tokenUrl="/api/tutores/login",
    scheme_name="Tutor_OAuth2"
)

oauth2_scheme_alumno = OAuth2PasswordBearer(
    tokenUrl="/api/alumnos/login",
    scheme_name="Alumno_OAuth2"
)


def get_admin_cualquier_rol(
    token: str = Depends(oauth2_scheme_admin),
    db: Session = Depends(get_session)
) -> Administrador:
    """
    Obtiene CUALQUIER administrador autenticado a partir del token JWT, sin importar su rol.
    
    Esta dependencia valida que el token sea correcto y el usuario exista.
    Se utiliza como base para `get_current_admin_user` y para endpoints que permiten
    acceso a roles específicos (como Psicología o Ciencias Básicas).
    
    Args:
        token: Token JWT del usuario autenticado.
        db: Sesión de base de datos.
    
    Returns:
        Instancia del modelo Administrador correspondiente al usuario autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario: Optional[str] = payload.get("sub")
        
        if usuario is None:
            raise credentials_exception
        
        token_data = TokenData(usuario=usuario)
    except JWTError:
        raise credentials_exception
    
    user = admin_service.get_admin_by_usuario(db, usuario=token_data.usuario) #type:ignore
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_admin_user(
    current_admin: Administrador = Depends(get_admin_cualquier_rol)
) -> Administrador:
    """
    Obtiene el administrador autenticado y VERIFICA que sea SUPER_ADMIN.
    
    Esta es la dependencia por defecto para proteger los endpoints administrativos existentes.
    Si el usuario tiene un rol limitado (ej. Psicología), esta función lanzará un error 403.
    
    Args:
        current_admin: El usuario administrador ya validado por get_admin_cualquier_rol.
    
    Returns:
        El administrador si es SUPER_ADMIN.
    
    Raises:
        HTTPException: Si el usuario no tiene permisos de Super Administrador.
    """
    # Validamos que el rol sea estrictamente SUPER_ADMIN
    if current_admin.rol != RolAdministrador.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de Super Administrador para realizar esta acción"
        )
    
    return current_admin


def get_current_tutor_user(
    token: str = Depends(oauth2_scheme_tutor),
    db: Session = Depends(get_session)
) -> Tutor:
    """
    Obtiene el tutor autenticado a partir del token JWT.
    
    Args:
        token: Token JWT del usuario autenticado.
        db: Sesión de base de datos.
    
    Returns:
        Instancia del modelo Tutor correspondiente al usuario autenticado.
    
    Raises:
        HTTPException: Si el token es inválido, el rol no es 'tutor' o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        role: Optional[str] = payload.get("role")
        
        if role is None or role != "tutor":
            raise credentials_exception
        
        tutor_id: Optional[str] = payload.get("sub")
        
        if tutor_id is None:
            raise credentials_exception
        
        token_data = TutorTokenData(id=tutor_id, role=role)
    except JWTError:
        raise credentials_exception
    
    if token_data.id is None:
        raise credentials_exception
    
    try:
        tutor_pk = int(token_data.id)
    except (ValueError, TypeError):
        raise credentials_exception
    
    user = db.get(Tutor, tutor_pk)
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme_tutor),
    db: Session = Depends(get_session)
) -> Union[Administrador, Tutor]:
    """
    Obtiene el usuario autenticado intentando validar como tutor primero y luego como administrador.
    
    Esta función permite endpoints que aceptan múltiples tipos de usuarios autenticados.
    
    Args:
        token: Token JWT del usuario autenticado.
        db: Sesión de base de datos.
    
    Returns:
        Instancia del modelo Tutor o Administrador según el tipo de usuario autenticado.
    
    Raises:
        HTTPException: Si el token es inválido para ambos roles o el usuario no existe.
    """
    try:
        tutor = get_current_tutor_user(token=token, db=db)
        return tutor
    except HTTPException as tutor_exc:
        if tutor_exc.status_code == 401:
            try:
                # Aquí usamos get_current_admin_user, por lo que requerirá SUPER_ADMIN por defecto.
                # Si necesitas que un usuario de rol limitado acceda a endpoints compartidos,
                # deberías cambiar esto a get_admin_cualquier_rol.
                admin = get_current_admin_user(current_admin=get_admin_cualquier_rol(token, db))
                return admin
            except HTTPException:
                raise tutor_exc
        else:
            raise tutor_exc
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas"
    )


def get_current_alumno_user(
    token: str = Depends(oauth2_scheme_alumno),
    db: Session = Depends(get_session)
) -> Alumno:
    """
    Obtiene el alumno autenticado a partir del token JWT.
    
    Args:
        token: Token JWT del usuario autenticado.
        db: Sesión de base de datos.
    
    Returns:
        Instancia del modelo Alumno correspondiente al usuario autenticado.
    
    Raises:
        HTTPException: Si el token es inválido, el rol no es 'alumno' o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        role: Optional[str] = payload.get("role")
        
        if role != "alumno":
            raise credentials_exception
        
        alumno_id_str: Optional[str] = payload.get("sub")
        
        if alumno_id_str is None:
            raise credentials_exception
        
        token_data = AlumnoTokenData(id=alumno_id_str, role=role)
    except JWTError:
        raise credentials_exception
    
    try:
        if token_data.id is None:
            raise credentials_exception
        
        alumno_pk = int(token_data.id)
    except (ValueError, TypeError):
        raise credentials_exception
    
    user = db.get(Alumno, alumno_pk)
    
    if user is None:
        raise credentials_exception
    
    return user