from sqlalchemy.orm import Session
from models.empresa import Empresa
from models.usuario_empresa import UsuarioEmpresa
from schemas.empresa import EmpresaCreate

def create_empresa(db: Session, empresa: EmpresaCreate):
    # Extraer usuario_id para crear la relación posterior
    empresa_data = empresa.model_dump()
    usuario_id = empresa_data.pop('usuario_id', None)
    
    print(f"DEBUG: Registrando empresa. usuario_id recibido: {usuario_id} (tipo: {type(usuario_id)})")
    
    try:
        # 1. Crear la empresa
        db_empresa = Empresa(**empresa_data)
        db.add(db_empresa)
        db.flush() # Obtener el ID de la empresa sin hacer commit todavía
        
        print(f"DEBUG: Empresa creada temporalmente con ID: {db_empresa.id}")
        
        # 2. Si viene un usuario_id, crear el vínculo automáticamente
        if usuario_id is not None:
            db_relacion = UsuarioEmpresa(
                usuario_id=int(usuario_id), 
                empresa_id=db_empresa.id,
                rol="ADMIN" # Por defecto el creador es ADMIN
            )
            db.add(db_relacion)
            print(f"DEBUG: Vínculo creado para usuario {usuario_id} y empresa {db_empresa.id}")
        else:
            print("WARNING: No se proporcionó usuario_id. La empresa se creará sin vínculo.")
            
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
        
    except Exception as e:
        db.rollback()
        print(f"ERROR al registrar empresa: {str(e)}")
        raise e

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
