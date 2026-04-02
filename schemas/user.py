from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    estado: str = "ACTIVO"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}
