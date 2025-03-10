from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Cours(Base):
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(Text, nullable=False)
    contenu = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relation avec les chapitres
    chapitres = relationship("Chapitre", back_populates="cours", cascade="all, delete-orphan")


class Chapitre(Base):
    __tablename__ = "chapitres"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(Text, nullable=False)
    contenu = Column(Text)
    cours_id = Column(Integer, ForeignKey("cours.id", ondelete="CASCADE"))  # Lien avec le cours

    # Relation avec le cours
    cours = relationship("Cours", back_populates="chapitres")
