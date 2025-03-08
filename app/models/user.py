from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from passlib.context import CryptContext
from app.models.base import user_reunion  # Importe la table d'association

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    adresse = Column(String(200))
    dob = Column(String(10))
    nationalite = Column(String(50))
    matrimonial = Column(String(50))
    sexe = Column(String(10))
    agence = Column(String(100))
    motivation = Column(Text)
    talent = Column(Text)
    occupation = Column(Text)
    nocturne = Column(String(50))
    implication = Column(String(50))
    password_hash = Column(String(255))
    is_admin = Column(Boolean, default=False)
    conduite = Column(Integer, default=100)
    profile_completed = Column(Boolean, default=False)
    role = Column(String(50), default='Membre')
    equipe_id = Column(Integer, ForeignKey('equipe.id'), nullable=True)
    equipe = relationship("Equipe", back_populates="users")
    staff = relationship("Staff", back_populates="users")
    points_history = relationship("PointsHistory", back_populates="user")
# Relation many-to-many avec Reunion
    reunion = relationship("Reunion", secondary=user_reunion, back_populates="users")
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)