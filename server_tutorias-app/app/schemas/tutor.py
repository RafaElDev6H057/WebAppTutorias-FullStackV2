# app/schemas/tutor.py

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

# --- Base Schema ---
class TutorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_p: str = Field(..., min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: EmailStr

    @field_validator('nombre', 'apellido_p', 'apellido_m', mode='before')
    def sanitize_text_fields(cls, v):
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Este campo no puede estar vacío.")
            return stripped
        return v

# --- Schemas for CRUD (Admin use) ---
class TutorCreate(TutorBase):
    contraseña: str = Field(..., min_length=8)

class TutorUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_p: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: Optional[EmailStr] = None
    contraseña: Optional[str] = None

    @field_validator('contraseña')
    def validate_new_password(cls, v):
        if v and len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres.')
        return v

# --- Schemas for Reading Data ---
class TutorRead(TutorBase):
    id_tutor: int
    requires_password_change: bool

    class Config:
        from_attributes = True

class TutorReadBasic(TutorBase): # Used for nested data in TutoriaReadWithDetails
    id_tutor: int
    requires_password_change: bool

    class Config:
        from_attributes = True

# --- Schemas for Authentication/Password Management (Tutor use) ---
class TutorLogin(BaseModel):
    correo: EmailStr
    contraseña: str

class TutorSetPassword(BaseModel): # For setting initial hashed password
    correo: EmailStr
    contraseña_actual: str # The temporary one
    nueva_contraseña: str = Field(..., min_length=8)

class TutorUpdatePassword(BaseModel): # For changing an existing hashed password
    contraseña_actual: str # The current hashed one
    nueva_contraseña: str = Field(..., min_length=8)

# --- Schema for Token Data ---
class TutorTokenData(BaseModel):
    id: Optional[str] = None # Corresponds to 'sub' in JWT, storing tutor ID
    role: Optional[str] = None # Should be 'tutor'