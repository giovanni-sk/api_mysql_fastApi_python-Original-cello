from sqlalchemy import Column, Integer, String, Text, Date, Time
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.base import user_reunion  # Importe la table d'association

class Reunion(Base):
    __tablename__ = 'reunion'

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100))  
    description = Column(Text)  
    date = Column(Date)  
    lieu = Column(String(255)) 
    heure = Column(Time)  
    color = Column(String(7))  
    # Relation many-to-many avec User
    users = relationship("User", secondary=user_reunion, back_populates="reunion")