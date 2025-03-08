from pydantic import BaseModel

class PointRequest(BaseModel):
    points: int
    motif: str