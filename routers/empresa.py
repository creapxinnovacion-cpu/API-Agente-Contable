from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from services import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/register", response_model=EmpresaResponse)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return empresa_service.create_empresa(db=db, empresa=empresa)

@router.get("/list", response_model=List[EmpresaResponse])
def list_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return empresa_service.get_empresas(db, skip=skip, limit=limit)

@router.get("/get/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = empresa_service.get_empresa(db, empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return db_empresa

@router.put("/update/{empresa_id}", response_model=EmpresaResponse)
def update_empresa(empresa_id: int, empresa: EmpresaUpdate, db: Session = Depends(get_db)):
    db_empresa = empresa_service.get_empresa(db, empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    updated_empresa = empresa_service.update_empresa(db, empresa_id, empresa.model_dump(exclude_unset=True))
    return updated_empresa

@router.delete("/delete/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = empresa_service.get_empresa(db, empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    empresa_service.delete_empresa(db, empresa_id)
    return {"status": "success", "mensaje": "Empresa eliminada exitosamente"}
