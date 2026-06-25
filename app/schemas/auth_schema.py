from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
import re

class UserRegister(BaseModel):
    """Schema para registrar un nuevo usuario."""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del usuario")
    email: str = Field(..., description="Email del usuario (debe ser válido)")
    password: str = Field(..., description="Contraseña segura")
    role: Optional[str] = Field(default="user", description="Rol del usuario (admin, support, user)")

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        """
        Valida que la contraseña cumpla con los requisitos de seguridad:
        - Mínimo 8 caracteres
        - Al menos una mayúscula
        - Al menos una minúscula
        - Al menos un número
        - Sin espacios en blanco
        """
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if ' ' in v:
            raise ValueError('La contraseña no puede contener espacios en blanco')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@example.com",
                "password": "Password123",
                "role": "user"
            }
        }
    )

class UserLogin(BaseModel):
    """Schema para iniciar sesión."""
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "ana@example.com",
                "password": "Password123"
            }
        }
    )

class Token(BaseModel):
    """Schema para la respuesta de token JWT."""
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }
    )

class TokenData(BaseModel):
    """Schema para los datos contenidos en el token JWT."""
    email: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)