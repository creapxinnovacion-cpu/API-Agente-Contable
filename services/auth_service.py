# services/auth_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from models.user import Usuario
from models.empresa import Empresa
from models.usuario_empresa import UsuarioEmpresa

from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

def create_user(email: str, password: str, db: Session):
    existing_user = db.query(Usuario).filter(Usuario.email == email).first()
    if existing_user:
        raise ValueError("El email ya está registrado")
        
    hashed_password = get_password_hash(password)
    
    db_user = Usuario(
        nombre=email.split('@')[0],
        email=email,
        password_hash=hashed_password,
        estado="ACTIVO"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
