from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.auth import LoginRequest, Token
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(request.email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extraer la empresa predeterminada/primera a la que pertenece el usuario
    empresa_activa_id = None
    nit_empresa = None
    if user.empresas and len(user.empresas) > 0:
        empresa_rel = user.empresas[0]
        if empresa_rel.empresa:
            empresa_activa_id = empresa_rel.empresa.id
            nit_empresa = empresa_rel.empresa.nit

    from datetime import timedelta
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Enriquecer el JWT con datos customizados para el FrontEnd
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": True if user.empresas and user.empresas[0].rol == "admin" else False,
        "empresaActiva": empresa_activa_id,
        "nitEmpresa": nit_empresa
    }
    
    token_response = auth_service.create_access_token(
        data=jwt_payload, expires_delta=access_token_expires
    )
    
    return token_response

@router.post("/register")
def register():
    return {"mensaje": "Endpoint de registro"}
