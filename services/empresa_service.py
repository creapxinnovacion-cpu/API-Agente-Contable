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

def get_empresa(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def update_empresa(db: Session, empresa_id: int, empresa_data: dict):
    db_empresa = get_empresa(db, empresa_id)
    if db_empresa:
        for key, value in empresa_data.items():
            if value is not None:
                setattr(db_empresa, key, value)
        db.commit()
        db.refresh(db_empresa)
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = get_empresa(db, empresa_id)
    if db_empresa:
        db.delete(db_empresa)
        db.commit()
    return db_empresa
