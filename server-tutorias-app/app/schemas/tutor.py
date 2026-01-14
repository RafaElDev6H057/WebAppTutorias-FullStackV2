"""
Esquemas Pydantic para validación y serialización de datos de Tutor.

Define los diferentes esquemas utilizados en las operaciones CRUD y autenticación
de tutores en el sistema de tutorías.
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, List


class TutorBase(BaseModel):
    """
    Esquema base con los campos comunes de Tutor.
    
    Incluye validaciones de longitud y sanitización de campos de texto.
    """
    
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_p: str = Field(..., min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: EmailStr
    
    @field_validator('nombre', 'apellido_p', 'apellido_m', mode='before')
    def sanitize_text_fields(cls, v):
        """
        Elimina espacios en blanco al inicio y final de campos de texto.
        
        Args:
            v: Valor del campo a sanitizar.
        
        Returns:
            Cadena sanitizada.
        
        Raises:
            ValueError: Si el campo está vacío después de eliminar espacios.
        """
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Este campo no puede estar vacío.")
            return stripped
        return v


class TutorCreate(TutorBase):
    """
    Esquema para la creación de un nuevo tutor.
    
    Incluye el campo de contraseña con validación de longitud mínima.
    """
    
    contraseña: str = Field(..., min_length=8)


class TutorUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un tutor.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_p: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    correo: Optional[EmailStr] = None
    contraseña: Optional[str] = None
    
    @field_validator('contraseña')
    def validate_new_password(cls, v):
        """
        Valida que la nueva contraseña tenga al menos 8 caracteres si se proporciona.
        
        Args:
            v: Nueva contraseña a validar.
        
        Returns:
            Contraseña validada o None si no se proporciona.
        
        Raises:
            ValueError: Si la contraseña proporcionada tiene menos de 8 caracteres.
        """
        if v and len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres.')
        return v


class TutorRead(TutorBase):
    """
    Esquema para lectura de datos de tutor.
    
    Incluye el identificador y el estado de cambio de contraseña.
    """
    
    id_tutor: int
    requires_password_change: bool
    
    model_config = ConfigDict(from_attributes=True)


class TutorReadBasic(TutorBase):
    """
    Esquema simplificado para lectura de tutor.
    
    Utilizado en respuestas anidadas como detalles de tutorías.
    """
    
    id_tutor: int
    requires_password_change: bool
    
    model_config = ConfigDict(from_attributes=True)


class TutorLogin(BaseModel):
    """Esquema para autenticación de tutor."""
    
    correo: EmailStr
    contraseña: str


class TutorSetPassword(BaseModel):
    """
    Esquema para establecer contraseña inicial de tutor.
    
    Requiere correo y contraseña temporal antes de establecer nueva.
    """
    
    correo: EmailStr
    contraseña_actual: str
    nueva_contraseña: str = Field(..., min_length=8)


class TutorUpdatePassword(BaseModel):
    """
    Esquema para actualización de contraseña de tutor autenticado.
    
    Requiere contraseña actual hasheada para confirmar identidad.
    """
    
    contraseña_actual: str
    nueva_contraseña: str = Field(..., min_length=8)


class TutorTokenData(BaseModel):
    """
    Datos extraídos del token JWT de un tutor.
    
    Attributes:
        id: Identificador del tutor (extraído del campo 'sub' del token).
        role: Rol del usuario en el sistema.
    """
    
    id: Optional[str] = None
    role: Optional[str] = None


class TutoresPage(BaseModel):
    """
    Esquema para respuesta paginada de tutores.
    
    Incluye el total de registros y la lista de tutores de la página actual.
    """
    
    total_tutores: int
    tutores: List[TutorRead]
