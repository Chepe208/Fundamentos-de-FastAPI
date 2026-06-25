from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserResponse
from app.auth.auth_service import register_user, authenticate_user, create_access_token_for_user
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    description="Crea un usuario con contraseña segura. Valida que el email sea único y la contraseña cumpla los requisitos."
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario.
    - **name**: Nombre completo (mínimo 3 caracteres).
    - **email**: Email válido y único.
    - **password**: Contraseña segura (mínimo 8 caracteres, mayúscula, minúscula, número, sin espacios).
    - **role**: (opcional) admin, support, user (por defecto user).
    """
    return register_user(db, user_data)

@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve un token JWT."
)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Inicia sesión con email y contraseña.
    - **email**: Email del usuario.
    - **password**: Contraseña del usuario.
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario autenticado",
    description="Retorna los datos del usuario autenticado usando el token JWT."
)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene la información del usuario autenticado.
    - Requiere token JWT en el encabezado: `Authorization: Bearer <token>`.
    - No retorna el campo `hashed_password`.
    """
    return current_user