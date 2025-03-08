from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Equipe(Base):
    __tablename__ = 'equipe'

    id = Column(Integer, primary_key=True, index=True)
    nom_equipe = Column(String(255))
    users = relationship("User", back_populates="equipe")