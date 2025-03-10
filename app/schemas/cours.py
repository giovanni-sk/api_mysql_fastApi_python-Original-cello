from pydantic import BaseModel,ConfigDict
from typing import Optional,List
from datetime import datetime

from app.schemas.chapitre import ChapitreResponse

class CoursBase(BaseModel):
    titre: str
    contenu: str

class CoursCreate(CoursBase):
    pass

class CoursUpdate(BaseModel):
    titre: Optional[str] = None
    contenu: Optional[str] = None

class CoursResponse(CoursCreate):
    id: int
    chapitres: List["ChapitreResponse"] = []

    model_config = ConfigDict(from_attributes=True)