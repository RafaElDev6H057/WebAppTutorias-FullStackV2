"""
Esquemas Pydantic para validación y serialización de datos de Administrador.

Define los diferentes esquemas utilizados en las operaciones CRUD, autenticación
y gestión de tokens JWT para administradores.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class AdministradorBase(BaseModel):
    """
    Esquema base con los campos comunes de Administrador.
    
    Incluye validaciones de formato y longitud para el nombre de usuario.
    """
    
    usuario: str = Field(
        ...,
        min_length=4,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    
    @field_validator('usuario', mode='before')
    def sanitize_usuario(cls, v):
        """
        Elimina espacios en blanco al inicio y final del nombre de usuario.
        
        Args:
            v: Valor del campo a sanitizar.
        
        Returns:
            Cadena sanitizada.
        """
        if isinstance(v, str):
            return v.strip()
        return v


class AdministradorCreate(AdministradorBase):
    """
    Esquema para la creación de un nuevo administrador.
    
    Incluye el campo de contraseña con validación de longitud mínima.
    """
    
    contraseña: str = Field(..., min_length=8)


class AdministradorUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un administrador.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    usuario: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    
    contraseña: Optional[str] = Field(default=None, min_length=8)


class AdministradorRead(AdministradorBase):
    """
    Esquema para lectura de datos de administrador.
    
    Incluye el identificador del administrador.
    """
    
    id_admin: int
    
    model_config = ConfigDict(from_attributes=True)


class AdministradorLogin(BaseModel):
    """Esquema para autenticación de administrador."""
    
    usuario: str
    contraseña: str


class Token(BaseModel):
    """
    Esquema de respuesta para tokens JWT.
    
    Utilizado en todas las operaciones de login del sistema.
    """
    
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Datos extraídos del token JWT de un administrador.
    
    Attributes:
        usuario: Nombre de usuario del administrador (extraído del campo 'sub' del token).
    """
    
    usuario: Optional[str] = None
