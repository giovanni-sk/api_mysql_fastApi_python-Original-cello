from pydantic import BaseModel
from typing import List

class AddUsersToEquipeRequest(BaseModel):
    users: List[int]
    
class EquipeBase(BaseModel):
    id:int
    nom_equipe: str
    
# Schéma pour la création d'une équipe (sans l'id)
class EquipeCreate(BaseModel):
    nom_equipe: str