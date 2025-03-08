from pydantic import BaseModel

class ReunionBase(BaseModel):
    titre: str
    description: str
    date: str
    lieu: str
    heure: str
    color: str

class ReunionGet(ReunionBase):
    id: int