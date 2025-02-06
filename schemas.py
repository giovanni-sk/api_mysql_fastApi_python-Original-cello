from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    nom: str
    prenom:str
    email :str
    adresse :str
    dob:str
    nationalite:str
    matrimonial:str
    sexe:str
    agence :str
    motivation :str
    talent :str
    occupation :str
    nocturne :str
    implication :str
    password :str
    is_admin: bool
    role :str
    conduite:int
    profile_completed:bool

class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    adresse: str
    dob: str
    nationalite: str
    matrimonial: str
    sexe: str
    agence: str
    motivation: str
    talent: str
    occupation: str
    nocturne: str
    implication: str
    is_admin: bool
    role:str
    conduite:int
    profile_completed:bool
    
    class Config:
        orm_mode = True

# Définir un modèle pour les données du login
class LoginRequest(BaseModel):
    email: str
    password: str    
        
class ReunionBase(BaseModel):
    titre:str
    description:str
    date:str
    lieu:str
    heure:str
    color:str   
    
class ReunionGet(ReunionBase):
    id:int
   
    
 # Modèle Pydantic pour les mises à jour partielles
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
    password :Optional[str] = None
    is_admin: Optional[bool ] = None
    role:Optional[str] = None
    conduite:Optional[int]=None
    profile_completed:Optional[bool]=None
    
    
class EmailSchema(BaseModel):
    email: List[EmailStr]   
    
    
class EquipeBase(BaseModel):
    nom_equipe:str
    
    
class StaffBase(BaseModel):
    nom:str
    prenom:str
    email: str
    telephone:str
    adresse:str
    
class StaffResponse(StaffBase):
    id: int
       