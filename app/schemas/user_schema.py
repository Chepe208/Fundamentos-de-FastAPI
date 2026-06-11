from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Email válido")
    role: RoleEnum = Field(default=RoleEnum.user, description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Email válido")
    role: Optional[RoleEnum] = Field(None, description="Rol del usuario")
    is_active: Optional[bool] = Field(None, description="Estado activo/inactivo")

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True