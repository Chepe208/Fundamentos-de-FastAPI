from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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