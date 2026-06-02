from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum
from app.services.user_service import obtener_todos, guardar_usuario, obtener_por_email
from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/", response_model=List[UserResponse])
async def listar_usuarios(
    role: Optional[RoleEnum] = None,
    is_active: Optional[bool] = None,
    response: Response = None
):
    usuarios = obtener_todos()
    if role:
        usuarios = [u for u in usuarios if u["role"] == role]
    if is_active is not None:
        usuarios = [u for u in usuarios if u["is_active"] == is_active]
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return usuarios

@router.get("/{user_id}", response_model=UserResponse)
async def obtener_usuario(
    user: dict = Depends(get_user_or_404),
    response: Response = None
):
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    user_data: UserCreate,
    response: Response
):
    if obtener_por_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    nuevo = guardar_usuario(user_data.model_dump())
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return nuevo