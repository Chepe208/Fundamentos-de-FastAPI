from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import (
    get_loans, get_loan_by_id, create_loan, return_loan,
    get_loans_with_details, get_loans_by_user, get_loans_by_device
)
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.models.user_model import User
from app.models.device_model import Device
from app.config.limiter import limiter 

router = APIRouter(prefix="/loans", tags=["Préstamos"])

@router.get(
    "/",
    response_model=List[LoanResponse],
    summary="Listar todos los préstamos",
    description="Obtiene una lista de todos los préstamos registrados en el sistema. Esta vista es simple y solo muestra los IDs de usuario y dispositivo, no los objetos completos.",
    response_description="Lista de préstamos con los campos básicos (id, user_id, device_id, loan_date, return_date, status)"
)
def list_loans(
    db: Session = Depends(get_db),
    response: Response = None
):
    loans = get_loans(db)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loans

@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    summary="Listar préstamos con detalles de usuario y dispositivo",
    description="Obtiene todos los préstamos con la información completa del usuario (nombre, email) y del dispositivo (nombre, serial, tipo, marca, disponibilidad). Permite filtrar por estado, email del usuario y tipo de dispositivo.",
    response_description="Lista de préstamos con datos anidados de usuario y dispositivo"
)
def get_loans_details(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    response: Response = None
):
    results = get_loans_with_details(db, status, user_email, device_type)

    loans = []
    for row in results:
        loans.append({
            "id": row.id,
            "loan_date": row.loan_date,
            "return_date": row.return_date,
            "status": row.status,
            "user_id": row.user_id,
            "device_id": row.device_id,
            "user": {
                "id": row.user_id,
                "name": row.user_name,
                "email": row.user_email
            },
            "device": {
                "id": row.device_id,
                "name": row.device_name,
                "serial_number": row.device_serial,
                "device_type": row.device_type,
                "brand": row.device_brand,
                "is_available": row.device_available
            }
        })
    
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loans

@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener un préstamo por ID",
    description="Retorna los detalles de un préstamo específico mediante su identificador. Si el préstamo no existe, devuelve un error 404.",
    response_description="Datos completos del préstamo solicitado"
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loan

@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo préstamo",
    description="Registra el préstamo de un dispositivo a un usuario. Valida que el usuario y el dispositivo existan, y que el dispositivo esté disponible. Si todo es correcto, cambia el estado del dispositivo a 'no disponible'.",
    response_description="Préstamo creado exitosamente con código 201"
)
@limiter.limit("10/minute")
def create_loan_endpoint(
    request: Request,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    response: Response = None,
    current_user: User = Depends(get_current_active_user)
):
    try:
        new_loan = create_loan(db, loan_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el préstamo")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return new_loan

@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver un dispositivo",
    description="Marca un préstamo activo como 'returned', asigna la fecha de devolución y cambia la disponibilidad del dispositivo a 'disponible'. Si el préstamo ya fue devuelto, devuelve error 409.",
    response_description="Préstamo actualizado (status: returned, return_date asignada, dispositivo disponible)"
)
def return_loan_endpoint(
    loan_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    try:
        updated_loan = return_loan(db, loan_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated_loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return updated_loan

@router.get(
    "/user/{user_id}/loans",
    response_model=List[LoanResponse],
    summary="Historial de préstamos de un usuario",
    description="Obtiene todos los préstamos (activos y devueltos) asociados a un usuario específico. Si el usuario no existe, devuelve error 404.",
    response_description="Lista de préstamos del usuario"
)
def get_loans_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    loans = get_loans_by_user(db, user_id)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loans

@router.get(
    "/device/{device_id}/loans",
    response_model=List[LoanResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Obtiene todos los préstamos (activos y devueltos) asociados a un dispositivo específico. Si el dispositivo no existe, devuelve error 404.",
    response_description="Lista de préstamos del dispositivo"
)
def get_loans_by_device_id(
    device_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    loans = get_loans_by_device(db, device_id)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loans