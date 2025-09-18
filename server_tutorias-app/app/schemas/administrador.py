# schemas/administrador.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AdministradorBase(BaseModel):
    # ✅ 1. Validación para el nombre de usuario
    usuario: str = Field(
        ..., 
        min_length=4, 
        max_length=100, 
        pattern=r"^[a-zA-Z0-9_]+$"  # Solo letras, números y guion bajo
    )
    
    @field_validator('usuario', mode='before')
    def sanitize_usuario(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class AdministradorCreate(AdministradorBase):
    # ✅ 2. Validación para la contraseña
    contraseña: str = Field(..., min_length=8)


class AdministradorUpdate(BaseModel):
    # ✅ 3. Aplicamos validaciones también a los campos opcionales
    usuario: Optional[str] = Field(
        default=None, 
        min_length=4, 
        max_length=100, 
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    contraseña: Optional[str] = Field(default=None, min_length=8)


class AdministradorRead(AdministradorBase):
    id_admin: int

    class Config:
        from_attributes = True


# Para login
class AdministradorLogin(BaseModel):
    usuario: str
    contraseña: str