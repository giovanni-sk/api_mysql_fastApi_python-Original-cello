from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.staff import StaffCreate, StaffResponse, StaffUpdate
from app.models.staff import Staff
from app.models.user import User
from app.db.session import get_db

router = APIRouter()

# Route pour créer un membre du staff
@router.post("/staff/{user_id}", response_model=StaffResponse, status_code=201)
async def create_staff(user_id: int, staff: StaffCreate, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Crée un nouveau membre du staff
    db_staff = Staff(**staff.dict(), user_id=user_id)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

# Route pour récupérer tous les membres du staff d'un utilisateur
@router.get("/user/{user_id}/staff", response_model=List[StaffResponse])
async def get_staff_by_user(user_id: int, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupère tous les membres du staff associés à cet utilisateur
    staffs = db.query(Staff).filter(Staff.user_id == user_id).all()
    return staffs

# Route pour récupérer un membre du staff par ID
@router.get("/staff/{staff_id}", response_model=StaffResponse)
async def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Membre du staff non trouvé")
    return db_staff

# Route pour mettre à jour un membre du staff
@router.put("/staff/{staff_id}", response_model=StaffResponse)
async def update_staff(staff_id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Membre du staff non trouvé")

    for key, value in staff.dict(exclude_unset=True).items():
        setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff

# Route pour supprimer un membre du staff
# Route pour supprimer un membre du staff d'un utilisateur spécifique
@router.delete("/user/{user_id}/staff/{staff_id}")
async def delete_staff(user_id: int, staff_id: int, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Vérifie si le membre du staff existe et appartient à l'utilisateur
    db_staff = db.query(Staff).filter(Staff.id == staff_id, Staff.user_id == user_id).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Membre du staff non trouvé ou n'appartient pas à cet utilisateur")

    # Supprime le membre du staff
    db.delete(db_staff)
    db.commit()
    
    return {"message": "Membre du staff supprimé avec succès"}
