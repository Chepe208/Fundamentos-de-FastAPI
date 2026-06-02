from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum, UserUpdate
from app.services.user_service import obtener_todos, guardar_usuario, obtener_por_email, actualizar_usuario_completo, actualizar_usuario_parcial, eliminar_usuario
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

@router.put("/{user_id}", response_model=UserResponse)
async def actualizar_usuario_put(
    user_id: int,
    user_data: UserCreate,
    response: Response
):

    existing = get_user_or_404(user_id)

    if user_data.email != existing["email"]:
        otro = obtener_por_email(user_data.email)
        if otro and otro["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado por otro usuario"
            )

    actualizado = actualizar_usuario_completo(user_id, user_data.model_dump())
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return actualizado

@router.patch("/{user_id}", response_model=UserResponse)
async def actualizar_usuario_patch(
    user_id: int,
    user_data: UserUpdate,
    response: Response
):
    existing = get_user_or_404(user_id)

    datos_parciales = user_data.model_dump(exclude_unset=True)
    
    if not datos_parciales:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar"
        )

    if "email" in datos_parciales:
        nuevo_email = datos_parciales["email"]
        if nuevo_email != existing["email"]:
            otro = obtener_por_email(nuevo_email)
            if otro and otro["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado por otro usuario"
                )
    actualizado = actualizar_usuario_parcial(user_id, datos_parciales)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return actualizado

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    user_id: int,
    response: Response
):
    get_user_or_404(user_id)
    
    from app.services.user_service import eliminar_usuario as eliminar_servicio
    if eliminar_servicio(user_id):
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
        return Response(status_code=status.HTTP_204_NO_CONTENT)