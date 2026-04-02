from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.sql import func

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
