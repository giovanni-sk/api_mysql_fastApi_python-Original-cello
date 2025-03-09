from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.points import PointsHistory
from app.schemas.points import PointRequest, PointsHistoryResponse
from typing import List

router = APIRouter()

@router.post("/user/{user_id}/moins", response_model=dict, status_code=200)
async def decrement_conduite(user_id: int, request: PointRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if request.points <= 0:
        raise HTTPException(status_code=400, detail="Le nombre de points à enlever doit être supérieur à 0")

    if user.conduite < request.points:
        raise HTTPException(status_code=400, detail="Nombre de points insuffisant")

    old_conduite = user.conduite
    user.conduite -= request.points

    # Enregistrer l'historique
    history_entry = PointsHistory(
        user_id=user.id,
        points=-request.points,  # Points négatifs pour indiquer un retrait
        motif=request.motif
    )
    db.add(history_entry)
    db.commit()
    db.refresh(user)

    return {
        "user_id": user.id,
        "old_conduite": old_conduite,
        "new_conduite": user.conduite,
        "points_removed": request.points,
        "motif": request.motif
    }

@router.post("/user/{user_id}/plus", response_model=dict, status_code=200)
async def increment_conduite(user_id: int, request: PointRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    old_conduite = user.conduite
    user.conduite += request.points

    # Enregistrer l'historique
    history_entry = PointsHistory(
        user_id=user.id,
        points=request.points,  # Points positifs pour indiquer un ajout
        motif=request.motif
    )
    db.add(history_entry)
    db.commit()
    db.refresh(user)

    return {
        "user_id": user.id,
        "old_conduite": old_conduite,
        "new_conduite": user.conduite,
        "points_added": request.points,
        "motif": request.motif
    }

@router.get("/user/{user_id}/history", response_model=List[PointsHistoryResponse], status_code=200)
async def get_history(user_id: int, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer l'historique des points de l'utilisateur
    historiques = db.query(PointsHistory).filter(PointsHistory.user_id == user_id).all()
    return historiques