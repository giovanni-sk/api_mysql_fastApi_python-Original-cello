from sqlalchemy import Table, Column, Integer,Boolean, ForeignKey
from app.db.session import Base

# Table d'association pour la relation many-to-many entre User et Reunion
user_reunion = Table(
    'user_reunion',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('reunion_id', Integer, ForeignKey('reunion.id'), primary_key=True),
    Column('present', Boolean, default=False)  # Marque la présence de l'utilisateur
)