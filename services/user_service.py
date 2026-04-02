# services/user_service.py
from sqlalchemy.orm import Session
from models.user import Usuario
from schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    # TODO: Hashear contraseña antes de guardar
    password_hash = user.password + "_hashed" 
    
    db_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        password_hash=password_hash,
        estado=user.estado
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()
