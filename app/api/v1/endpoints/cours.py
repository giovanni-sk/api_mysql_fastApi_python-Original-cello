from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.cours import CoursCreate, CoursResponse, CoursUpdate
from app.schemas.chapitre import ChapitreCreate, ChapitreResponse
from app.models.cours import Cours,Chapitre
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


# Ajouter un chapitre à un cours
@router.post("/cours/{cours_id}/chapitre", response_model=ChapitreResponse, status_code=201)
async def add_chapitre(cours_id: int, chapitre: ChapitreCreate, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == cours_id).first()
    if not db_cours:
        raise HTTPException(status_code=404, detail="Cours non trouvé")

    db_chapitre = Chapitre(**chapitre.dict(), cours_id=cours_id)
    db.add(db_chapitre)
    db.commit()
    db.refresh(db_chapitre)
    return db_chapitre


# Récupérer un cours avec ses chapitres
@router.get("/cours/{cours_id}", response_model=CoursResponse)
async def get_cours(cours_id: int, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == cours_id).first()
    if not db_cours:
        raise HTTPException(status_code=404, detail="Cours non trouvé")
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
# Modifier un chapitre
@router.put("/chapitre/{chapitre_id}", response_model=ChapitreResponse)
async def update_chapitre(chapitre_id: int, chapitre: ChapitreCreate, db: Session = Depends(get_db)):
    db_chapitre = db.query(Chapitre).filter(Chapitre.id == chapitre_id).first()
    if not db_chapitre:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")

    db_chapitre.titre = chapitre.titre
    db_chapitre.contenu = chapitre.contenu

    db.commit()
    db.refresh(db_chapitre)
    return db_chapitre

# Supprimer un chapitre
@router.delete("/chapitre/{chapitre_id}")
async def delete_chapitre(chapitre_id: int, db: Session = Depends(get_db)):
    db_chapitre = db.query(Chapitre).filter(Chapitre.id == chapitre_id).first()
    if not db_chapitre:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")

    db.delete(db_chapitre)
    db.commit()
    return {"message": "Chapitre supprimé avec succès"}

# Route pour supprimer un cours
@router.delete("/cours/{id}")
async def delete_cours(id: int, db: Session = Depends(get_db)):
    db_cours = db.query(Cours).filter(Cours.id == id).first()
    if db_cours is None:
        raise HTTPException(status_code=404, detail="Cours non trouvé")

    db.delete(db_cours)
    db.commit()
    return {"message": "Cours supprimé avec succès"}