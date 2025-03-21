from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.equipe import EquipeBase,EquipeCreate,AddUsersToEquipeRequest
from app.models.equipe import Equipe
from app.db.session import get_db

router = APIRouter()

# Créer une équipe
@router.post("/equipe", response_model=EquipeBase)
async def create_equipe(equipe: EquipeCreate, db: Session = Depends(get_db)):
    db_equipe = Equipe(**equipe.dict())
    db.add(db_equipe)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

# Récupérer une équipe par son ID
@router.get("/equipe/{id}", response_model=EquipeBase)
async def read_equipe(id: int, db: Session = Depends(get_db)):
    db_equipe = db.query(Equipe).filter(Equipe.id == id).first()
    if not db_equipe:
        raise HTTPException(status_code=404, detail="Équipe non trouvée")
    return db_equipe

# Récupérer toutes les équipes
@router.get("/equipes", response_model=List[EquipeBase])
async def read_all_equipes(db: Session = Depends(get_db)):
    equipes = db.query(Equipe).all()
    return equipes

# Mettre à jour une équipe
@router.put("/equipe/{id}", response_model=EquipeBase)
async def update_equipe(id: int, equipe: EquipeCreate, db: Session = Depends(get_db)):
    db_equipe = db.query(Equipe).filter(Equipe.id == id).first()
    if not db_equipe:
        raise HTTPException(status_code=404, detail="Équipe non trouvée")
    for key, value in equipe.dict().items():
        setattr(db_equipe, key, value)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

# Supprimer une équipe
@router.delete("/equipe/{id}")
async def delete_equipe(id: int, db: Session = Depends(get_db)):
    db_equipe = db.query(Equipe).filter(Equipe.id == id).first()
    if not db_equipe:
        raise HTTPException(status_code=404, detail="Équipe non trouvée")
    db.delete(db_equipe)
    db.commit()
    return {"message": "Équipe supprimée avec succès"}

# Ajouter des membres à une équipe
@router.post("/equipe/{id}/users", response_model=dict)
async def add_users_to_equipe(
    id: int,
    request: AddUsersToEquipeRequest,
    db: Session = Depends(get_db)
):
    users = request.users  # Accédez à la liste des utilisateurs
    equipe = db.query(Equipe).filter(Equipe.id == id).first()
    if not equipe:
        raise HTTPException(status_code=404, detail="Équipe non trouvée")

    # Vérifier si les utilisateurs existent et ne sont pas déjà dans une équipe
    valid_users = db.query(User).filter(User.id.in_(users)).all()
    if len(valid_users) != len(users):
        raise HTTPException(status_code=400, detail="Un ou plusieurs utilisateurs sont introuvables")

    for user in valid_users:
        if user.equipe_id is not None:
            raise HTTPException(status_code=400, detail=f"L'utilisateur {user.id} est déjà dans une équipe")

    # Vérifier que l'équipe ne dépasse pas 5 membres
    existing_users = db.query(User).filter(User.equipe_id == id).count()
    if existing_users + len(users) > 5:
        raise HTTPException(status_code=400, detail="Une équipe ne peut pas avoir plus de 5 membres")

    # Ajouter les utilisateurs à l'équipe
    for user in valid_users:
        user.equipe_id = id
        db.add(user)

    db.commit()
    return {"message": "Utilisateurs ajoutés avec succès", "equipe_id": id}
# Récupérer les utilisateurs d'une équipe
@router.get("/equipe/{id}/users", response_model=List[UserResponse])
async def get_users_in_equipe(id: int, db: Session = Depends(get_db)):
    equipe = db.query(Equipe).filter(Equipe.id == id).first()
    if not equipe:
        raise HTTPException(status_code=404, detail="Équipe non trouvée")
    users_in_equipe = db.query(User).filter(User.equipe_id == id).all()
    return users_in_equipe

# Retirer un utilisateur d'une équipe
@router.delete("/equipe/{id}/users/{user_id}")
async def remove_user_from_equipe(id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.equipe_id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé dans cette équipe")
    user.equipe_id = None
    db.commit()
    return {"message": "Utilisateur retiré de l'équipe avec succès"}


# Récupérer tous les utilisateurs disponibles (non assignés à une équipe)
@router.get("/users/available", response_model=List[UserResponse])
async def get_available_users(db: Session = Depends(get_db)):
    available_users = db.query(User).filter(User.equipe_id.is_(None)).all()
    return available_users