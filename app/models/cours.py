from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Cours(Base):
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(Text)
    contenu = Column(Text)
    created_at = Column(DateTime, default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())