"""
Esquemas Pydantic para validación y serialización de datos de Alumno.

Define los diferentes esquemas utilizados en las operaciones CRUD y autenticación
de alumnos en el sistema de tutorías.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import List, Optional


class AlumnoBase(BaseModel):
    """
    Esquema base con los campos comunes de Alumno.
    
    Incluye validaciones de longitud y sanitización de campos de texto.
    """
    
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_p: str = Field(..., min_length=2, max_length=100)
    apellido_m: Optional[str] = None
    num_control: str = Field(..., max_length=50)
    carrera: str = Field(..., min_length=3, max_length=100)
    semestre_actual: int = Field(..., ge=1, le=14)
    estado: str
    telefono: Optional[str] = None
    correo: EmailStr
    
    @field_validator('nombre', 'apellido_p', 'apellido_m', 'carrera', mode='before')
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


class AlumnoCreate(AlumnoBase):
    """
    Esquema para la creación de un nuevo alumno.
    
    Incluye el campo de contraseña con validación de longitud mínima.
    """
    
    contraseña: str = Field(..., min_length=8)


class AlumnoUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un alumno.
    
    Todos los campos son opcionales y solo los proporcionados serán actualizados.
    """
    
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_p: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido_m: Optional[str] = Field(default=None, max_length=100)
    num_control: Optional[str] = Field(default=None, max_length=50)
    contraseña: Optional[str] = None
    carrera: Optional[str] = Field(default=None, min_length=3, max_length=100)
    semestre_actual: Optional[int] = Field(default=None, ge=1, le=14)
    estado: Optional[str] = None
    telefono: Optional[str] = Field(default=None, max_length=100)
    correo: Optional[EmailStr] = None
    
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


class AlumnoRead(AlumnoBase):
    """
    Esquema para lectura de datos de alumno.
    
    Incluye el identificador y el estado de cambio de contraseña.
    """
    
    id_alumno: int
    requires_password_change: bool
    
    model_config = ConfigDict(from_attributes=True)


class AlumnoLogin(BaseModel):
    """Esquema para autenticación de alumno."""
    
    num_control: str
    contraseña: str


class AlumnoReadBasic(AlumnoBase):
    """
    Esquema simplificado para lectura de alumno.
    
    No incluye información sensible como el estado de cambio de contraseña.
    """
    
    id_alumno: int
    
    model_config = ConfigDict(from_attributes=True)


class AlumnoSetPassword(BaseModel):
    """
    Esquema para establecer contraseña inicial de alumno.
    
    Requiere número de control y contraseña actual antes de establecer nueva.
    """
    
    num_control: str
    contraseña_actual: str
    nueva_contraseña: str = Field(..., min_length=8)


class AlumnoUpdatePassword(BaseModel):
    """
    Esquema para actualización de contraseña de alumno autenticado.
    
    Requiere contraseña actual para confirmar identidad.
    """
    
    contraseña_actual: str
    nueva_contraseña: str = Field(..., min_length=8)


class AlumnosPage(BaseModel):
    """
    Esquema para respuesta paginada de alumnos.
    
    Incluye el total de registros y la lista de alumnos de la página actual.
    """
    
    total_alumnos: int
    alumnos: List[AlumnoRead]


class AlumnoTokenData(BaseModel):
    """
    Datos extraídos del token JWT de un alumno.
    
    Attributes:
        id: Identificador del alumno (extraído del campo 'sub' del token).
        role: Rol del usuario en el sistema.
    """
    
    id: Optional[str] = None
    role: Optional[str] = None


class AlumnoTutoriaStatus(BaseModel):
    """
    Estado de progreso de tutorías de un alumno.
    
    Attributes:
        tutorias_completadas: Número de tutorías completadas por el alumno.
        es_elegible: Indica si el alumno es elegible para continuar (>= 4 tutorías).
    """
    
    tutorias_completadas: int
    es_elegible: bool
