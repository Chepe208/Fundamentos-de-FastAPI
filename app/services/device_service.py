from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch
from typing import Optional
from app.models.loan_model import Loan

def create_device(db: Session, device_data: DeviceCreate) -> Device:
    db_device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand,
        is_available=device_data.is_available
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%")
            )
        )
    return query.all()

def get_device_by_id(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()

def update_device(db: Session, device_id: int, device_data: DeviceUpdate) -> Device | None:
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return None
    db_device.name = device_data.name
    db_device.serial_number = device_data.serial_number
    db_device.device_type = device_data.device_type
    db_device.brand = device_data.brand
    db_device.is_available = device_data.is_available
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device_partial(db: Session, device_id: int, device_data: DevicePatch) -> Device | None:
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return None
    update_data = device_data.model_dump(exclude_unset=True)
    if not update_data:
        return db_device
    for field, value in update_data.items():
        setattr(db_device, field, value)
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int) -> bool:
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return False

    loans = db.query(Loan).filter(Loan.device_id == device_id).all()
    if loans:
        return "has_loans" 

    db.delete(db_device)
    db.commit()
    return True