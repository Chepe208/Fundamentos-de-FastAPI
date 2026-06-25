from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPatch, RoleEnum
from app.services.user_service import (
    crear_usuario, obtener_todos, obtener_por_id, obtener_por_email,
    actualizar_usuario_completo, actualizar_usuario_parcial, eliminar_usuario,
    filtrar_por_rol, filtrar_por_estado, filtrar_por_rol_y_estado
)
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/", response_model=List[UserResponse])
def listar_usuarios(
    role: Optional[RoleEnum] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    response: Response = None,
    current_user: User = Depends(get_current_active_user)
):
    if role and is_active is not None:
        usuarios = filtrar_por_rol_y_estado(db, role.value, is_active)
    elif role:
        usuarios = filtrar_por_rol(db, role.value)
    elif is_active is not None:
        usuarios = filtrar_por_estado(db, is_active)
    else:
        usuarios = obtener_todos(db)
    
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return usuarios

@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    response: Response = None,
    current_user: User = Depends(get_current_active_user)
):
    usuario = obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return usuario

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    response: Response = None
):
    if obtener_por_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo = crear_usuario(db, user_data)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return nuevo

@router.put("/{user_id}", response_model=UserResponse)
def actualizar_usuario_completo_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    response: Response = None
):
    existing = obtener_por_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user_data.email != existing.email and obtener_por_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado por otro usuario")
    actualizado = actualizar_usuario_completo(db, user_id, user_data)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return actualizado

@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_usuario_parcial_endpoint(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
    response: Response = None
):
    existing = obtener_por_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un campo para actualizar")
    if "email" in update_data and update_data["email"] != existing.email:
        if obtener_por_email(db, update_data["email"]):
            raise HTTPException(status_code=400, detail="El email ya está registrado por otro usuario")
    actualizado = actualizar_usuario_parcial(db, user_id, user_data)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return actualizado

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    if not eliminar_usuario(db, user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return None