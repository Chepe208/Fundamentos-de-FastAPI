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

@router.get("/", response_model=List[UserResponse])
async def listar_usuarios(
    role: Optional[RoleEnum] = None,
    is_active: Optional[bool] = None
):
    """
    Lista todos los usuarios. Permite filtrar por role y por is_active.
    """
    resultados = usuarios_db.copy()
    
    if role:
        resultados = [u for u in resultados if u["role"] == role]
    if is_active is not None:
        resultados = [u for u in resultados if u["is_active"] == is_active]
    
    return resultados

@router.get("/{user_id}", response_model=UserResponse)
async def obtener_usuario(user_id: int):
    """
    Obtiene un usuario por su ID.
    """
    usuario = buscar_por_id(user_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_usuario(
    user_data: UserCreate,
    response: Response
):
    """
    Registra un nuevo usuario. Valida que el email no exista.
    """
    global next_id
    
    # Verificar email duplicado
    if buscar_por_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear diccionario con ID
    nuevo_usuario = user_data.model_dump()
    nuevo_usuario["id"] = next_id
    next_id += 1
    
    # Guardar en "BD"
    usuarios_db.append(nuevo_usuario)
    
    # Enviar cabeceras personalizadas
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    
    return nuevo_usuario