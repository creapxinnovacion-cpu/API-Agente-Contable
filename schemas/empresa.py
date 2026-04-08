from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    nit: str
    nombre_razon_social: str
    correo: Optional[str] = None
    estado: str = "ACTIVA"

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nit: Optional[str] = None
    nombre_razon_social: Optional[str] = None
    correo: Optional[str] = None
    estado: Optional[str] = None

class EmpresaResponse(EmpresaBase):
    id: int

    model_config = {"from_attributes": True}
