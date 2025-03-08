from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cours import CoursBase, CoursResponse
from app.models.cours import Cours
from app.db.session import get_db

router = APIRouter()

@router.post("/cours", response_model=CoursResponse)
async def create_cours(cours: CoursBase, db: Session = Depends(get_db)):
    # Implémente la logique pour créer un cours
    pass

@router.get("/cours/{id}", response_model=CoursResponse)
async def read_cours(id: int, db: Session = Depends(get_db)):
    # Implémente la logique pour récupérer un cours par ID
    pass