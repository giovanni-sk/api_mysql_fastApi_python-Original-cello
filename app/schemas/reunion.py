from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date
from enum import Enum

class ReunionBase(BaseModel):
    titre: str = Field(..., max_length=100)
    description: str = Field(...)
    date: date
    lieu: str = Field(..., max_length=255)
    heure: str
    color: str = Field(..., max_length=7)

    @field_validator('heure')
    @classmethod
    def validate_time_format(cls, v):
        try:
            parts = v.split(':')
            
            # Si format HH:MM (2 parties)
            if len(parts) == 2:
                hours, minutes = map(int, parts)
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    raise ValueError("Valeurs d'heure invalides")
                # Ajouter les secondes
                return f"{hours:02d}:{minutes:02d}:00"
                
            # Si format HH:MM:SS (3 parties)
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                    raise ValueError("Valeurs d'heure invalides")
                return v
            else:
                raise ValueError("Le format de l'heure doit être HH:MM ou HH:MM:SS")
            
        except Exception as e:
            raise ValueError(f"Format d'heure invalide: {str(e)}")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "titre": "Réunion importante",
                "description": "Discussion sur les objectifs trimestriels",
                "date": "2023-10-15",
                "lieu": "Salle de conférence A",
                "heure": "14:00:00",
                "color": "#3788d8"
            }
        }
    }

# Si vous avez besoin de classes pour la réponse avec ID
class ReunionResponse(ReunionBase):
    id: int
    
    
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }


# Si vous avez besoin de classes pour la création/mise à jour avec des champs optionnels
class ReunionUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None # type: ignore
    lieu: Optional[str] = None
    heure: Optional[str] = None
    color: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }
    
    
    
    
    
    
    

class StatutPresence(str, Enum):
    PRESENT = "present(e)"
    ABSENT = "absent(e)"
    PERMISSIONNAIRE = "permissionnaire"

class PresenceUpdate(BaseModel):
    user_id: int
    statut: StatutPresence
    commentaire: str = "Aucun motif pour son absence"

class PresenceUpdateRequest(BaseModel):
    presences: List[PresenceUpdate]

class PresenceResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    statut: StatutPresence
    commentaire: str