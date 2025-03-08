from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipe import EquipeBase
from app.models.equipe import Equipe
from app.db.session import get_db

router = APIRouter()

@router.post("/equipe", response_model=EquipeBase)
async def create_equipe(equipe: EquipeBase, db: Session = Depends(get_db)):
    # Implémente la logique pour créer une équipe
    pass

@router.get("/equipe/{id}", response_model=EquipeBase)
async def read_equipe(id: int, db: Session = Depends(get_db)):
    # Implémente la logique pour récupérer une équipe par ID
    pass