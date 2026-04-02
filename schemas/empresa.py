from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    nit: str
    nombre_razon_social: str
    correo: Optional[str] = None
    estado: str = "ACTIVA"

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int

    model_config = {"from_attributes": True}
