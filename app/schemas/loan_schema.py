from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBasicInfo(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class DeviceBasicInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Estado del préstamo: active, returned, overdue")

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True

class LoanDetailResponse(LoanResponse):
    user: UserBasicInfo
    device: DeviceBasicInfo