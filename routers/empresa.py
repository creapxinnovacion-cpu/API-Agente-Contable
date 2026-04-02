from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.empresa import EmpresaCreate, EmpresaResponse
from services import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=EmpresaResponse)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return empresa_service.create_empresa(db=db, empresa=empresa)

@router.get("/", response_model=List[EmpresaResponse])
def get_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return empresa_service.get_empresas(db, skip=skip, limit=limit)
