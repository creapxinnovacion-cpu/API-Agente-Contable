from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Text
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    estado = Column(String(20), default="ACTIVO")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relación a la tabla intermedia
    empresas = relationship("UsuarioEmpresa", back_populates="usuario")
