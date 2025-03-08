from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import ConfigDict

class UserBase(BaseModel):
    nom: str
    prenom: str 
    email: EmailStr
    adresse: Optional[str] = None
    dob: Optional[str] = None
    nationalite: Optional[str] = None
    matrimonial: Optional[str] = None
    sexe: Optional[str] = None
    agence: Optional[str] = None
    motivation: Optional[str] = None
    talent: Optional[str] = None
    occupation: Optional[str] = None
    nocturne: Optional[str] = None
    implication: Optional[str] = None
    password: str
    is_admin: bool = False
    role: str = "Membre"
    conduite: int = 100
    profile_completed: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    adresse: Optional[str] = None
    dob: Optional[str] = None
    nationalite: Optional[str] = None
    matrimonial: Optional[str] = None
    sexe: Optional[str] = None
    agence: Optional[str] = None
    motivation: Optional[str] = None
    talent: Optional[str] = None
    occupation: Optional[str] = None
    nocturne: Optional[str] = None
    implication: Optional[str] = None
    is_admin: bool
    role: str
    conduite: int
    profile_completed: bool

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    adresse: Optional[str] = None
    dob: Optional[str] = None
    nationalite: Optional[str] = None
    matrimonial: Optional[str] = None
    sexe: Optional[str] = None
    agence: Optional[str] = None
    motivation: Optional[str] = None
    talent: Optional[str] = None
    occupation: Optional[str] = None
    nocturne: Optional[str] = None
    implication: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    role: Optional[str] = None
    conduite: Optional[int] = None
    profile_completed: Optional[bool] = None