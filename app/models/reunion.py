from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Text
from app.db.session import Base
from sqlalchemy.orm import relationship
from app.models.base import user_reunion  # Importe la table d'association


class Reunion(Base):
    __tablename__ = "reunion"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    lieu = Column(String(255), nullable=False)
    heure = Column(String(8), nullable=False)
    color = Column(String(7), nullable=False)
    users = relationship("User", secondary=user_reunion, back_populates="reunion")
    
    