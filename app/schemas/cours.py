from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime

class CoursBase(BaseModel):
    titre: str
    contenu: str

class CoursCreate(CoursBase):
    pass

class CoursUpdate(BaseModel):
    titre: Optional[str] = None
    contenu: Optional[str] = None

class CoursResponse(CoursBase):
    id: int
    created_at: datetime
    # updated_at: datetime

    model_config = ConfigDict(from_attributes=True)