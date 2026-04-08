from pydantic import BaseModel
from typing import Optional

class UsuarioEmpresaBase(BaseModel):
    usuario_id: int
    empresa_id: int
    rol: str = "CONTADOR"

class UsuarioEmpresaCreate(UsuarioEmpresaBase):
    pass

class UsuarioEmpresaUpdate(BaseModel):
    rol: Optional[str] = None

class UsuarioEmpresaResponse(UsuarioEmpresaBase):
    id: int

    model_config = {"from_attributes": True}

class UsuarioEmpresaDetail(BaseModel):
    relacion_id: int
    usuario_id: int
    nombre: str
    email: str
    empresa_id: int
    nombre_razon_social: str
    nit: str
    rol: str

    model_config = {"from_attributes": True}
