from pydantic import BaseModel
from pydantic import ConfigDict

class CoursBase(BaseModel):
    titre: str
    Contenu: str

    model_config = ConfigDict(from_attributes=True)

class CoursResponse(CoursBase):
    id: int