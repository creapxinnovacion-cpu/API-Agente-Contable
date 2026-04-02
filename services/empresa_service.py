# services/empresa_service.py
from sqlalchemy.orm import Session
from models.empresa import Empresa
from schemas.empresa import EmpresaCreate

def create_empresa(db: Session, empresa: EmpresaCreate):
    db_empresa = Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def get_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Empresa).offset(skip).limit(limit).all()
