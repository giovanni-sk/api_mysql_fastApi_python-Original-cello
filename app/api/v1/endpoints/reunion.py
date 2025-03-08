from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reunion import ReunionBase, ReunionGet
from app.models.reunion import Reunion
from app.db.session import get_db

router = APIRouter()

@router.post("/reunion", response_model=ReunionGet)
async def create_reunion(reunion: ReunionBase, db: Session = Depends(get_db)):
    # Implémente la logique pour créer une réunion
    pass

@router.get("/reunion/{id}", response_model=ReunionGet)
async def read_reunion(id: int, db: Session = Depends(get_db)):
    # Implémente la logique pour récupérer une réunion par ID
    pass