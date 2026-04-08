from sqlalchemy.orm import Session
from models.usuario_empresa import UsuarioEmpresa
from models.user import Usuario
from models.empresa import Empresa
from schemas.usuario_empresa import UsuarioEmpresaCreate

def create_usuario_empresa(db: Session, usuario_empresa: UsuarioEmpresaCreate):
    db_relacion = UsuarioEmpresa(**usuario_empresa.model_dump())
    db.add(db_relacion)
    db.commit()
    db.refresh(db_relacion)
    return db_relacion

def get_usuario_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UsuarioEmpresa).offset(skip).limit(limit).all()

def get_usuario_empresas_detallado(db: Session, skip: int = 0, limit: int = 100):
    resultado = db.query(
        UsuarioEmpresa.id.label("relacion_id"),
        Usuario.id.label("usuario_id"),
        Usuario.nombre,
        Usuario.email,
        Empresa.id.label("empresa_id"),
        Empresa.nombre_razon_social,
        Empresa.nit,
        UsuarioEmpresa.rol
    ).join(
        Usuario, UsuarioEmpresa.usuario_id == Usuario.id
    ).join(
        Empresa, UsuarioEmpresa.empresa_id == Empresa.id
    ).offset(skip).limit(limit).all()
    
    # row es un objeto Row o tupla, lo pasamos a un diccionario o lo devolvemos para que Pydantic haga from_attributes
    return resultado

def get_usuario_empresa(db: Session, id: int):
    return db.query(UsuarioEmpresa).filter(UsuarioEmpresa.id == id).first()

def update_usuario_empresa(db: Session, id: int, data: dict):
    db_relacion = get_usuario_empresa(db, id)
    if db_relacion:
        for key, value in data.items():
            if value is not None:
                setattr(db_relacion, key, value)
        db.commit()
        db.refresh(db_relacion)
    return db_relacion

def delete_usuario_empresa(db: Session, id: int):
    db_relacion = get_usuario_empresa(db, id)
    if db_relacion:
        db.delete(db_relacion)
        db.commit()
    return db_relacion
