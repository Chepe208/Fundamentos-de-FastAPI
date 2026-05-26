from pydantic import BaseModel, Field, field_validator, EmailStr
from enum import Enum
from typing import Optional

# Enum para los roles permitidos
class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Modelo base
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Email válido")
    role: RoleEnum = Field(default=RoleEnum.user, description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")

# Modelo para crear usuario
class UserCreate(UserBase):
    pass

# Modelo para respuesta
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True