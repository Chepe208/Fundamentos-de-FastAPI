from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate
from typing import Optional

def get_loans(db: Session):
    return db.query(Loan).all()

def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    return db.query(Loan).filter(Loan.id == loan_id).first()

def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
    # Validar que el usuario existe
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise ValueError("Dispositivo no encontrado")

    if not device.is_available:
        raise ValueError("El dispositivo no está disponible para préstamo")

    new_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        loan_date=datetime.now(),
        status="active"
    )
    db.add(new_loan)

    device.is_available = False
    
    db.commit()
    db.refresh(new_loan)
    return new_loan

def return_loan(db: Session, loan_id: int) -> Loan | None:
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        return None

    if loan.status == "returned":
        raise ValueError("El préstamo ya fue devuelto anteriormente")

    loan.status = "returned"
    loan.return_date = datetime.now()
    
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    
    db.commit()
    db.refresh(loan)
    return loan

def get_loans_with_details(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    query = db.query(
        Loan.id,
        Loan.loan_date,
        Loan.return_date,
        Loan.status,
        User.id.label("user_id"),
        User.name.label("user_name"),
        User.email.label("user_email"),
        Device.id.label("device_id"),
        Device.name.label("device_name"),
        Device.serial_number.label("device_serial"),
        Device.device_type.label("device_type"),
        Device.brand.label("device_brand"),
        Device.is_available.label("device_available")
    ).join(User, Loan.user_id == User.id)\
     .join(Device, Loan.device_id == Device.id)

    if status:
        query = query.where(Loan.status == status)
    if user_email:
        query = query.where(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.where(Device.device_type == device_type)

    return query.all()

def get_loans_by_user(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def get_loans_by_device(db: Session, device_id: int):
    return db.query(Loan).filter(Loan.device_id == device_id).all()