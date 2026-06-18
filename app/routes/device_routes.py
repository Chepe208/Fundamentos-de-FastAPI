from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services.device_service import (
    create_device,
    get_devices,
    get_device_by_id,
    update_device,
    update_device_partial,
    delete_device
)
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

@router.get("/", response_model=List[DeviceResponse])
def list_devices(
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    response: Response = None
):
    devices = get_devices(db, device_type, is_available, brand, search)
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return device

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device_endpoint(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    response: Response = None
):
    try:
        new_device = create_device(db, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado"
        )
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return new_device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device_endpoint(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    response: Response = None
):
    existing = get_device_by_id(db, device_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    try:
        updated = update_device(db, device_id, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado por otro dispositivo"
        )
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return updated

@router.patch("/{device_id}", response_model=DeviceResponse)
def patch_device_endpoint(
    device_id: int,
    device_data: DevicePatch,
    db: Session = Depends(get_db),
    response: Response = None
):
    existing = get_device_by_id(db, device_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    update_data = device_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar"
        )
    try:
        updated = update_device_partial(db, device_id, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado por otro dispositivo"
        )
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return updated

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_endpoint(
    device_id: int,
    db: Session = Depends(get_db),
    response: Response = None
):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if response:
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "1.0"
    return None