from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    telephone = Column(String(200))
    adresse = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="staff")