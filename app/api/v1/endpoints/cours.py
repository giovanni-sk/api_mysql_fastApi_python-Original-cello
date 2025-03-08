from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.cours import CoursCreate, CoursResponse, CoursUpdate
from app.models.cours import Cours
from app.db.session import get_db

router = APIRouter()

# Route pour créer un cours
@router.post("/cours", response_model=CoursResponse, status_code=201)
async def create_cours(cours: CoursCreate, db: Session = Depends(get_db)):
    db_cours = Cours(**cours.dict())
    db.add(db_cours)
    db.commit()
    db.refresh(db_cours)
    return db_cours

# Route pour récupérer tous les cours
@router.get("/cours", response_model=List[CoursResponse])
async def get_all_cours(db: Session = Depends(get_db)):
    cours = db.query(Cours).all()
    return cours

# Route pour récupérer un cours par ID
@router.get("/cours/{id}", response_model=CoursResponse)
async def get_cours_by_id(id: int, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == id).first()
    if db_cours is None:
        raise HTTPException(status_code=404, detail="Cours non trouvé")
    return db_cours

# Route pour mettre à jour un cours
@router.put("/cours/{id}", response_model=CoursResponse)
async def update_cours(id: int, cours: CoursUpdate, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == id).first()
    if db_cours is None:
        raise HTTPException(status_code=404, detail="Cours non trouvé")

    for key, value in cours.dict(exclude_unset=True).items():
        setattr(db_cours, key, value)

    # db_cours.updated_at = datetime.utcnow()  # Met à jour la date de modification
    db.commit()
    db.refresh(db_cours)
    return db_cours

# Route pour supprimer un cours
@router.delete("/cours/{id}")
async def delete_cours(id: int, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == id).first()
    if db_cours is None:
        raise HTTPException(status_code=404, detail="Cours non trouvé")

    db.delete(db_cours)
    db.commit()
    return {"message": "Cours supprimé avec succès"}