from pydantic import BaseModel,ConfigDict
from typing import Optional

class ChapitreCreate(BaseModel):
    titre: str
    contenu: Optional[str] = None

class ChapitreResponse(ChapitreCreate):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
