from pydantic import BaseModel
from datetime import datetime

class PointsHistoryBase(BaseModel):
    user_id: int
    points: int
    motif: str

class PointsHistoryCreate(PointsHistoryBase):
    pass

class PointsHistory(PointsHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  