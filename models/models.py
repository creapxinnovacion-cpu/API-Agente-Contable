from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base
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

    # Relación con la tabla intermedia
    usuarios = relationship("UsuarioEmpresa", back_populates="empresa")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    estado = Column(String(20), default="ACTIVO")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relación con la tabla intermedia
    empresas = relationship("UsuarioEmpresa", back_populates="usuario")


class UsuarioEmpresa(Base):
    __tablename__ = "usuario_empresas"

    id = Column(BigInteger, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    rol = Column(String(20), default="CONTADOR")
    
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint('usuario_id', 'empresa_id', name='uq_usuario_empresa'),
    )

    usuario = relationship("Usuario", back_populates="empresas")
    empresa = relationship("Empresa", back_populates="usuarios")
