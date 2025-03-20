from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional

class ReunionBase(BaseModel):
    titre: str = Field(..., max_length=100, description="Le titre de la réunion")
    description: str = Field(..., description="La description de la réunion")
    date: datetime = Field(..., description="La date de la réunion au format YYYY-MM-DD")
    lieu: str = Field(..., max_length=255, description="Le lieu de la réunion")
    heure: time = Field(..., description="L'heure de la réunion au format HH:MM:SS")
    color: str = Field(..., max_length=7, description="La couleur de la réunion au format hexadécimal")


    class Config:
        json_schema_extra = {
            "example": {
                "titre": "Réunion importante",
                "description": "Discussion sur les objectifs trimestriels",
                "date": "2023-10-15",
                "lieu": "Salle de conférence A",
                "heure": "14:00:00",
                "color": "#3788d8",
            }
        }