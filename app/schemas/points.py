from pydantic import BaseModel
from datetime import datetime


class PointRequest(BaseModel):
    points: int  # Nombre de points à ajouter ou retirer
    motif: str   # Raison de la modification
    
class PointsHistoryResponse(BaseModel):
    id: int
    user_id: int
    points: int
    motif: str
    created_at: datetime

    class Config:
        from_attributes = True  # Anciennement `orm_mode = True`