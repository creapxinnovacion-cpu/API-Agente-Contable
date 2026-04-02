from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.sql import func

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(BigInteger, primary_key=True, index=True)
    nombre_razon_social = Column(String(255), nullable=False)
    nit = Column(String(20), unique=True, index=True, nullable=False)
    correo = Column(String(150))
    estado = Column(String(20), default="ACTIVA")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relación a la tabla intermedia
    usuarios = relationship("UsuarioEmpresa", back_populates="empresa")
