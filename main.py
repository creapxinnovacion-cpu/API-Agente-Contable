from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.database import engine, get_db
from db.base import Base

import models.user
import models.empresa
import models.usuario_empresa

from routers import auth, users, empresa

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
# Swagger UI ya viene incluido por defecto en el endpoint `/docs`
app = FastAPI(
    title="API Agente Contable",
    description="Backend para la plataforma SaaS de contabilidad y procesamiento DTE",
    version="1.0.0",
    docs_url="/docs",  # URL de Swagger UI
    redoc_url="/redoc" # URL de ReDoc (alternativa a Swagger)
)

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173", # Vite por defecto
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(empresa.router)

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "mensaje": "Bienvenido a la API de Agente Contable",
        "docs": "Visita /docs para ver la documentación de Swagger"
    }

@app.get("/health", tags=["Salud"])
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint para verificar que la API y la conexión a la base de datos están funcionando.
    """
    try:
        # Intenta hacer una consulta simple a la base de datos para probar la conexión
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    return {
        "api_status": "ok",
        "db_status": db_status
    }
# endpoint de get de validacion de credenciales de usuarios
@app.get("/login", tags=["Autenticación"])
def login_get(email: str, password: str, db: Session = Depends(get_db)):
    from services import auth_service
    user = auth_service.authenticate_user(email, password, db)
    
    if not user:
        return {"status": "error", "mensaje": "Credenciales incorrectas"}
        
    return {
        "status": "success",
        "mensaje": "Válido",
        "datos": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email
        }
    }
