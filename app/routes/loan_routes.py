from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import get_loans, get_loan_by_id, create_loan, return_loan
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/loans", tags=["Préstamos"])

@router.get("/", response_model=List[LoanResponse])
def list_loans(
    db: Session = Depends(get_db),
    response: Response = None
):
    loans = get_loans(db)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return loans

@router.get("/{loan_id}", response_model=LoanResponse)
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

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan_endpoint(
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    response: Response = None
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

@router.patch("/{loan_id}/return", response_model=LoanResponse)
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