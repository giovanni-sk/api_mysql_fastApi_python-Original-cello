from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from typing import List
from app.schemas.reunion import ReunionBase,ReunionResponse,PresenceUpdateRequest
from app.models.reunion import Reunion
from app.models.user import User
from app.db.session import get_db
from app.models.base import user_reunion


router = APIRouter()

@router.post("/reunions/{reunion_id}/presences")
def update_presences(
    reunion_id: int, 
    presence_data: PresenceUpdateRequest, 
    db: Session = Depends(get_db)
):
    # Vérifier si la réunion existe
    reunion = db.query(Reunion).filter(Reunion.id == reunion_id).first()
    if reunion is None:
        raise HTTPException(status_code=404, detail="Réunion non trouvée")

    # Mettre à jour les présences pour chaque participant
    for presence in presence_data.presences:
        # Vérifier que l'utilisateur est bien un participant à la réunion
        existing_participation = db.query(user_reunion).filter(
            user_reunion.c.reunion_id == reunion_id,
            user_reunion.c.user_id == presence.user_id
        ).first()

        if existing_participation is None:
            raise HTTPException(status_code=400, detail=f"L'utilisateur {presence.user_id} n'est pas un participant à cette réunion")

        # Convertir le statut en chaîne de caractères avec une longueur limitée
        statut_str = str(presence.statut.value)[:20]  # Limite à 20 caractères

        # Mettre à jour la présence
        db.execute(
            user_reunion.update()
            .where(
                (user_reunion.c.reunion_id == reunion_id) & 
                (user_reunion.c.user_id == presence.user_id)
            )
            .values(
                statut_presence=statut_str, 
                commentaire=presence.commentaire or "Aucun motif pour son absence"
            )
        )
    
    db.commit()
    return {"detail": "Présences mises à jour avec succès"}



# Route pour créer une réunion
@router.post("/reunion", response_model=ReunionBase, status_code=201)
async def create_reunion(reunion: ReunionBase, db: Session = Depends(get_db)):
    try:
        # 1. Création de la réunion
        db_reunion = Reunion(**reunion.dict())
        db.add(db_reunion)
        db.commit()
        db.refresh(db_reunion)

        # 2. Récupération des utilisateurs
        users = db.query(User).all()

        # 3. Insertion des utilisateurs dans `user_reunion` avec statut par défaut
        insert_stmt = insert(user_reunion).values([
            {"user_id": user.id, "reunion_id": db_reunion.id, "statut_presence": "absent(e)", "commentaire": "Aucun motif pour son absence"}
            for user in users
        ])

        # 4. Exécution et validation
        db.execute(insert_stmt)
        db.commit()

        return db_reunion

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reunions/{reunion_id}/presences")
def get_presences(
    reunion_id: int, 
    db: Session = Depends(get_db)
):
    # Vérifier si la réunion existe
    reunion = db.query(Reunion).filter(Reunion.id == reunion_id).first()
    if reunion is None:
        raise HTTPException(status_code=404, detail="Réunion non trouvée")
    
    # Récupérer tous les utilisateurs
    all_users = db.query(User).all()
    
    # Récupérer les présences existantes
    existing_presences = db.execute(
        select(user_reunion.c.user_id, 
               user_reunion.c.statut_presence, 
               user_reunion.c.commentaire)
        .where(user_reunion.c.reunion_id == reunion_id)
    ).fetchall()
    
    # Créer un dictionnaire de présences existantes
    presences_dict = {
        presence.user_id: {
            "statut": presence.statut_presence,
            "commentaire": presence.commentaire
        } for presence in existing_presences
    }
    
    # Construire la réponse finale
    return [
        {
            "id": user.id,
            "nom": user.nom,
            "prenom": user.prenom,
            "statut": presences_dict.get(user.id, {}).get('statut', 'absent(e)'),
            "commentaire": presences_dict.get(user.id, {}).get('commentaire', 'Aucun motif pour son absence')
        } for user in all_users
    ]    
# Route pour récupérer toutes les réunions
@router.get("/reunion", response_model=List[ReunionResponse])
async def get_all_reunions(db: Session = Depends(get_db)):
   try:
        reunions = db.query(Reunion).all()
        return reunions

   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route pour récupérer une réunion par ID
@router.get("/reunion/{id}", response_model=ReunionResponse)
async def get_reunion_by_id(id: int, db: Session = Depends(get_db)):
   try: 
        reunion = db.query(Reunion).filter(Reunion.id == id).first()
        if reunion is None:
            raise HTTPException(status_code=404, detail="Réunion non trouvée")
        return reunion
   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       
# Route pour mettre à jour une réunion
@router.put("/reunion/{id}", response_model=ReunionResponse, status_code=200)
async def update_reunion(id: int, reunion:ReunionResponse, db: Session = Depends(get_db)):
   try:
        db_reunion = db.query(Reunion).filter(Reunion.id == id).first()
        if db_reunion is None:
            raise HTTPException(status_code=404, detail="Réunion non trouvée")
        
        for key, value in reunion.dict(exclude_unset=True).items():
            setattr(db_reunion, key, value)
            
        db.commit()
        db.refresh(db_reunion)
        return db_reunion
   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour supprimer une réunion
@router.delete("/reunion/{id}")
async def delete_reunion(id: int, db: Session = Depends(get_db)):
    try:
        db_reunion = db.query(Reunion).filter(Reunion.id == id).first()
        if db_reunion is None:
            raise HTTPException(status_code=404, detail="Réunion non trouvée")

        db.delete(db_reunion)
        db.commit()
        return {"message": "Réunion supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))