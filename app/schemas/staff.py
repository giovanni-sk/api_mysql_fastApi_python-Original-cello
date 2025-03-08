from pydantic import BaseModel
from typing import Optional

class StaffBase(BaseModel):
    nom: str
    prenom: str
    email: str
    telephone: str
    adresse: str

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None

class StaffResponse(StaffBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Anciennement `orm_mode = True` dans Pydantic V1