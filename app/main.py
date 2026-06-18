from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router  # <--- NUEVO
from app.database.connection import engine, Base

# Importar modelos para que Alembic los registre
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios, dispositivos y préstamos",
    version="2.0.0"
)

app.include_router(user_router)
app.include_router(device_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API"}