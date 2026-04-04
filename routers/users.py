from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.auth import LoginRequest
from services.auth_service import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# endpoint de get de validacion de credenciales de usuarios
@router.get("/login", tags=["Autenticación"])
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
