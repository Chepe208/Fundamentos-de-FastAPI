from fastapi import APIRouter, HTTPException, status, Response
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Base de datos en memoria
usuarios_db = []
next_id = 1

# Función auxiliar para buscar por email
def buscar_por_email(email: str):
    for u in usuarios_db:
        if u["email"] == email:
            return u
    return None

# Función auxiliar para buscar por id
def buscar_por_id(user_id: int):
    for u in usuarios_db:
        if u["id"] == user_id:
            return u
    return None