from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class PointsHistory(Base):
    __tablename__ = "points_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    points = Column(Integer, nullable=False)  # +X ou -X
    motif = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relation avec User
    user = relationship("User", back_populates="points_history")