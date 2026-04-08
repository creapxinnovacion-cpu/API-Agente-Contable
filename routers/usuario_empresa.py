from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.usuario_empresa import UsuarioEmpresaCreate, UsuarioEmpresaResponse, UsuarioEmpresaUpdate, UsuarioEmpresaDetail
from services import usuario_empresa_service

router = APIRouter(prefix="/usuario-empresas", tags=["Usuarios-Empresas"])

@router.post("/register", response_model=UsuarioEmpresaResponse)
def create_usuario_empresa(relacion: UsuarioEmpresaCreate, db: Session = Depends(get_db)):
    try:
        return usuario_empresa_service.create_usuario_empresa(db=db, usuario_empresa=relacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear relacion. Posible duplicado de usuario_id y empresa_id")

@router.get("/list", response_model=List[UsuarioEmpresaDetail])
def list_usuario_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return usuario_empresa_service.get_usuario_empresas_detallado(db, skip=skip, limit=limit)

@router.get("/get/{relacion_id}", response_model=UsuarioEmpresaResponse)
def get_usuario_empresa(relacion_id: int, db: Session = Depends(get_db)):
    db_relacion = usuario_empresa_service.get_usuario_empresa(db, relacion_id)
    if db_relacion is None:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    return db_relacion

@router.put("/update/{relacion_id}", response_model=UsuarioEmpresaResponse)
def update_usuario_empresa(relacion_id: int, relacion: UsuarioEmpresaUpdate, db: Session = Depends(get_db)):
    db_relacion = usuario_empresa_service.get_usuario_empresa(db, relacion_id)
    if db_relacion is None:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    
    updated_relacion = usuario_empresa_service.update_usuario_empresa(db, relacion_id, relacion.model_dump(exclude_unset=True))
    return updated_relacion

@router.delete("/delete/{relacion_id}")
def delete_usuario_empresa(relacion_id: int, db: Session = Depends(get_db)):
    db_relacion = usuario_empresa_service.get_usuario_empresa(db, relacion_id)
    if db_relacion is None:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    
    usuario_empresa_service.delete_usuario_empresa(db, relacion_id)
    return {"status": "success", "mensaje": "Relacion eliminada exitosamente"}
