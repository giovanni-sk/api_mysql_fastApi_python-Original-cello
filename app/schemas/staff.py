from pydantic import BaseModel

class StaffBase(BaseModel):
    nom: str
    prenom: str
    email: str
    telephone: str
    adresse: str

class StaffResponse(StaffBase):
    id: int