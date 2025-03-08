from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.base import user_reunion  # Importe la table d'association


class Reunion(Base):
    __tablename__ = 'reunion'

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(50))
    description = Column(String(255))
    date = Column(String(100))
    lieu = Column(String(255))
    heure = Column(String(100))
    color = Column(String(100))
    users = relationship("User", secondary=user_reunion, back_populates="reunion")