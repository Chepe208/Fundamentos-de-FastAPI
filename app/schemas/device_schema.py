from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del dispositivo")
    serial_number: str = Field(..., min_length=3, max_length=50, description="Número de serie único")
    device_type: str = Field(..., description="Tipo de dispositivo: laptop, tablet, proyector, cámara, router, monitor")
    brand: Optional[str] = Field(None, max_length=50, description="Marca del dispositivo (opcional)")
    is_available: bool = Field(default=True, description="Disponibilidad para préstamo")

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DevicePatch(BaseModel):  # <--- NUEVO SCHEMA PARA PATCH
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=3, max_length=50)
    device_type: Optional[str] = Field(None)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = Field(None)

class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True