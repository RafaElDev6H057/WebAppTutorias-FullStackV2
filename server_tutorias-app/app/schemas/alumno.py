# schemas/alumno.py

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional

# Importamos el Enum definido en el modelo para reutilizarlo
# from app.models.alumno import EstadoAlumno 

# 💡 Idea: Podríamos preguntarle al usuario el formato exacto de su num_control
# Por ahora, un ejemplo: 8 dígitos numéricos.
# Ejemplo: r"^\d{8}$"  (una 'r' antes de las comillas indica un raw string)

class AlumnoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_p: str = Field(..., min_length=2, max_length=100)
    apellido_m: Optional[str] = None
    num_control: str = Field(..., max_length=50)
    carrera: str = Field(..., min_length=3, max_length=100)
    semestre_actual: int = Field(..., ge=1, le=14)
    estado: str
    curp: str = Field(..., min_length=18, max_length=18)
    correo: EmailStr

    # ✅ 4. (Opcional pero recomendado) Sanitizar entradas de texto
    @field_validator('nombre', 'apellido_p', 'apellido_m', 'carrera', mode='before')
    def sanitize_text_fields(cls, v):
        if isinstance(v, str):
            # Elimina espacios en blanco al inicio/final y previene strings vacíos
            stripped = v.strip()
            if not stripped:
                raise ValueError("Este campo no puede estar vacío.")
            return stripped
        return v

class AlumnoCreate(AlumnoBase):
    # ✅ 5. Validación de longitud mínima para la contraseña
    contraseña: str = Field(..., min_length=8)


class AlumnoUpdate(BaseModel):
    # Aplicamos las mismas validaciones a los campos opcionales
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_p: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    num_control: Optional[str] = Field(default=None, max_length=50)
    
    # ✅ 1. Eliminamos min_length de aquí para manejarlo con un validador personalizado
    contraseña: Optional[str] = None 
    
    carrera: Optional[str] = Field(default=None, min_length=3, max_length=100)
    semestre_actual: Optional[int] = Field(default=None, ge=1, le=14)
    estado: Optional[str] = None
    curp: Optional[str] = Field(default=None, min_length=18, max_length=18)
    correo: Optional[EmailStr] = None
    
    # ✅ 2. Añadimos un validador que solo se activa si se escribe una nueva contraseña
    @field_validator('contraseña')
    def validate_new_password(cls, v):
        # Si 'v' no es None y no es un string vacío...
        if v and len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres.')
        # Si es None o "", se permite.
        return v
    
    # (El sanitizador de AlumnoBase no se hereda, si se quisiera, habría que añadirlo aquí también)


class AlumnoRead(AlumnoBase):
    id_alumno: int
    requires_password_change: bool

    class Config:
        from_attributes = True


class AlumnoLogin(BaseModel):
    num_control: str
    contraseña: str

class AlumnoReadBasic(AlumnoBase):
    id_alumno: int

    class Config:
        from_attributes = True

class AlumnoSetPassword(BaseModel):
    num_control: str
    contraseña_actual: str
    nueva_contraseña: str = Field(..., min_length=8)