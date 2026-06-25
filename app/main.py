from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router 
from app.auth.auth_routes import router as auth_router 
from app.database.connection import engine, Base

from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan


app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios, dispositivos y préstamos",
    version="2.0.0",
    contact={"name": "Jose Manuel Ruiz Zapata", "email": "jruizzapata38@gmail.com"},
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API"}