from fastapi import APIRouter, Depends, HTTPException 
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.points import PointsHistory
from app.schemas.points import PointsHistoryCreate, PointsHistoryBase
from app.models.user import User

router = APIRouter()

@router.post("/points", response_model=PointsHistoryBase, status_code=201)
async def add_points(points: PointsHistoryCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == points.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Convertir le schéma Pydantic en modèle SQLAlchemy
    db_points = PointsHistory(**points.dict())

    # Ajouter l'instance à la session
    db.add(db_points)
    db.commit()
    db.refresh(db_points)

    # Mettre à jour le total des points de l'utilisateur
    user.conduite += points.points
    db.commit()

    return db_points


@router.get("/points/{user_id}", response_model=List[PointsHistoryBase])
async def get_points_history(user_id: int, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer l'historique des points de l'utilisateur
    points_history = db.query(PointsHistory).filter(PointsHistory.user_id == user_id).all()
    return points_history