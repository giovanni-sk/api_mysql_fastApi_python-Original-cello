from sqlalchemy import Table, Column, Integer,Enum,Text,ForeignKey
from app.db.session import Base


# Table d'association pour la relation many-to-many entre User et Reunion
user_reunion = Table(
    'user_reunion',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('reunion_id', Integer, ForeignKey('reunion.id'), primary_key=True),
    Column('statut_presence',Enum("absent(e)", "present(e)", "permissionnaire", name="statut_presence_enum"), default="absent(e)"),
    Column('commentaire',Text,default="Aucun motif pour son absence")
)