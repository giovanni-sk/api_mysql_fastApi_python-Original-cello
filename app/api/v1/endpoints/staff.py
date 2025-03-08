from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.staff import StaffBase, StaffResponse
from app.models.staff import Staff
from app.db.session import get_db

router = APIRouter()

@router.post("/staff", response_model=StaffResponse)
async def create_staff(staff: StaffBase, db: Session = Depends(get_db)):
    # Implémente la logique pour créer un staff
    pass

@router.get("/staff/{id}", response_model=StaffResponse)
async def read_staff(id: int, db: Session = Depends(get_db)):
    # Implémente la logique pour récupérer un staff par ID
    pass