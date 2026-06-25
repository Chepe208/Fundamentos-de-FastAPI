from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta

def register_user(db: Session, user_data: UserRegister) -> User:
    """
    Registra un nuevo usuario en la base de datos.
    Valida que el email no esté duplicado.
    Hashea la contraseña antes de guardarla.
    """

    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    hashed = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed,
        role=user_data.role or "user",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Autentica un usuario verificando su email y contraseña.
    Retorna el usuario si las credenciales son válidas, o None en caso contrario.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token_for_user(user: User) -> str:
    """
    Crea un token JWT para el usuario autenticado.
    Incluye el email, rol y user_id en el payload.
    """
    data = {
        "sub": user.email,
        "role": user.role,
        "user_id": user.id
    }
    return create_access_token(data)