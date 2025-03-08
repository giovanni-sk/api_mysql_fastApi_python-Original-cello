from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.points import PointRequest
from app.models.points import PointsHistory
from app.db.session import get_db

router = APIRouter()

@router.post("/points", response_model=PointRequest)
async def add_points(request: PointRequest, db: Session = Depends(get_db)):
    # Implémente la logique pour ajouter des points
    pass

@router.get("/points/{id}", response_model=PointRequest)
async def read_points(id: int, db: Session = Depends(get_db)):
    # Implémente la logique pour récupérer des points par ID
    pass