from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.auth import LoginRequest
from services import auth_service

router = APIRouter(prefix="/users", tags=["Usuarios"])

# endpoint de get de validacion de credenciales de usuarios
@router.get("/login", tags=["Usuarios"])
def login_get(email: str, password: str, db: Session = Depends(get_db)):
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
#endpoint de crear usuarios
@router.post("/register", tags=["Usuarios"])
def register(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.create_user(request.email, request.password, db)
    return {
        "status": "success",
        "mensaje": "Usuario creado exitosamente",
        "datos": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email
        }
    } 
#endpoint de actualizar usuarios
@router.put("/update", tags=["Usuarios"])
def update(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.update_user(request.email, request.password, db)
    return {
        "status": "success",
        "mensaje": "Usuario actualizado exitosamente",
        "datos": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email
        }
    }   
#endpoint de eliminar usuarios
@router.delete("/delete", tags=["Usuarios"])
def delete(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.delete_user(request.email, request.password, db)
    return {
        "status": "success",
        "mensaje": "Usuario eliminado exitosamente",
        "datos": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email
        }
    }   
#endpoint de listar usuarios
@router.get("/list", tags=["Usuarios"])
def list(db: Session = Depends(get_db)):
    users = auth_service.list_users(db)
    return {
        "status": "success",
        "mensaje": "Usuarios listados exitosamente",
        "datos": users
    }   