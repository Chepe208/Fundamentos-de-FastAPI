from fastapi import HTTPException, status
from app.services.user_service import obtener_por_id

def get_user_or_404(user_id: int):
    usuario = obtener_por_id(user_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario