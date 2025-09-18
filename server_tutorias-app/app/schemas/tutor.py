# schemas/tutor.py

from pydantic import BaseModel, Field, EmailStr, field_validator # 👈 Importamos EmailStr y field_validator
from typing import Optional

class TutorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_p: str = Field(..., min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=100)
    
    # ✅ 1. Validación automática de formato de correo electrónico
    correo: EmailStr
    
    # ✅ 2. Validación de formato de teléfono (ej. 10 dígitos numéricos)
    telefono: str = Field(..., pattern=r"^\d{10}$")

    # ✅ 3. (Opcional pero recomendado) Sanitizar entradas de texto
    @field_validator('nombre', 'apellido_p', 'apellido_m', 'especialidad', mode='before')
    def sanitize_text_fields(cls, v):
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Este campo no puede estar vacío.")
            return stripped
        return v

class TutorCreate(TutorBase):
    # ✅ 4. Validación de longitud mínima para la contraseña
    contraseña: str = Field(..., min_length=8)

class TutorUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_p: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    especialidad: Optional[str] = Field(default=None, min_length=3, max_length=100)
    correo: Optional[EmailStr] = None
    
    # ✅ 1. Eliminamos min_length para manejarlo con un validador
    contraseña: Optional[str] = None 
    
    telefono: Optional[str] = Field(default=None, pattern=r"^\d{10}$")

    # ✅ 2. Añadimos el validador personalizado para la nueva contraseña
    @field_validator('contraseña')
    def validate_new_password(cls, v):
        # Si 'v' no es None y no es un string vacío...
        if v and len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres.')
        # Si es None o "", se permite.
        return v

class TutorRead(TutorBase):
    id_tutor: int

    class Config:
        from_attributes = True

class TutorLogin(BaseModel):
    correo: EmailStr
    contraseña: str

class TutorReadBasic(TutorBase):
    id_tutor: int

    class Config:
        from_attributes = True