from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

def crear_usuario(db: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role.value,
        is_active=user_data.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def obtener_todos(db: Session, skip: int = 0, limit: int = 100):
    """Retorna todos los usuarios (con paginación básica)."""
    return db.query(User).offset(skip).limit(limit).all()

def obtener_por_id(db: Session, user_id: int) -> User | None:
    """Busca un usuario por su ID. Retorna None si no existe."""
    return db.query(User).filter(User.id == user_id).first()

def obtener_por_email(db: Session, email: str) -> User | None:
    """Busca un usuario por su email. Retorna None si no existe."""
    return db.query(User).filter(User.email == email).first()

def actualizar_usuario_completo(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    """Reemplaza todos los campos de un usuario existente."""
    db_user = obtener_por_id(db, user_id)
    if not db_user:
        return None
    db_user.name = user_data.name
    db_user.email = user_data.email
    db_user.role = user_data.role.value
    db_user.is_active = user_data.is_active
    db.commit()
    db.refresh(db_user)
    return db_user

def actualizar_usuario_parcial(db: Session, user_id: int, user_data: UserPatch) -> User | None:
    """Actualiza solo los campos proporcionados en la petición PATCH."""
    db_user = obtener_por_id(db, user_id)
    if not db_user:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        return db_user 
    for field, value in update_data.items():
        if field == "role" and value is not None:
            value = value.value  # convertir Enum a str
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def eliminar_usuario(db: Session, user_id: int) -> bool:
    """Elimina un usuario de la base de datos. Retorna True si se eliminó, False si no existía."""
    db_user = obtener_por_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def filtrar_por_rol(db: Session, role: str):
    """Retorna usuarios que coincidan con el rol dado."""
    return db.query(User).filter(User.role == role).all()

def filtrar_por_estado(db: Session, is_active: bool):
    """Retorna usuarios activos o inactivos."""
    return db.query(User).filter(User.is_active == is_active).all()

def filtrar_por_rol_y_estado(db: Session, role: str, is_active: bool):
    """Combina ambos filtros."""
    return db.query(User).filter(User.role == role, User.is_active == is_active).all()

def obtener_ordenados_por_nombre(db: Session, ascending: bool = True):
    """Retorna usuarios ordenados por nombre (ascendente por defecto)."""
    if ascending:
        return db.query(User).order_by(User.name.asc()).all()
    return db.query(User).order_by(User.name.desc()).all()

def obtener_ordenados_por_fecha(db: Session, ascending: bool = True):
    """Retorna usuarios ordenados por fecha de creación (ascendente por defecto)."""
    if ascending:
        return db.query(User).order_by(User.created_at.asc()).all()
    return db.query(User).order_by(User.created_at.desc()).all()