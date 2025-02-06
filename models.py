from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey,Table
from sqlalchemy.orm import relationship
from database import Base
from passlib.context import CryptContext

# Initialisation de CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Table d'association pour la relation many-to-many entre User et Reunion
user_reunion = Table(
    'user_reunion',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('reunion_id', Integer, ForeignKey('reunion.id'), primary_key=True),
    Column('present', Boolean, default=False)  # Marque la présence de l'utilisateur
)


# Table Utilisateur
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    adresse = Column(String(200))
    dob = Column(String(10))  # Exemple format date, ajustez si nécessaire
    nationalite = Column(String(50))
    matrimonial = Column(String(50))
    sexe = Column(String(10))
    agence = Column(String(100))
    motivation = Column(Text)
    talent = Column(Text)
    occupation = Column(Text)
    nocturne = Column(String(50))
    implication = Column(String(50))
    password_hash = Column(String(255))  # Stockage sécurisé du mot de passe
    is_admin = Column(Boolean, default=False)  # Définit si l'utilisateur est admin
    conduite = Column(Integer,default=100) #conduite de l'utilisateur
    profile_completed = Column(Boolean, default=False) #si le profil est complété
    # Ajout d'un rôle au sein de l'équipe
    role = Column(String(50), nullable=False)  # Responsable, Adjoint, Secrétaire, Membres_simple
    # Relation many-to-many avec Reunion
    reunion = relationship("Reunion",secondary=user_reunion, back_populates="users")
 # Clé étrangère pour l'équipe
    equipe_id = Column(Integer, ForeignKey('equipe.id'), nullable=True)
    equipe = relationship("Equipe", back_populates="users")
# Relation avec Staff
    staff = relationship("Staff", back_populates="users")

 

    # Méthode pour vérifier le mot de passe
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
   
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

#    Table Reunion
class Reunion(Base):
    __tablename__ = 'reunion'

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(50))
    description=Column(String(255))
    date = Column(String(100))
    lieu = Column(String(255))
    heure = Column(String(100))
    color = Column(String(100))
    # Relation many-to-many avec User
    users = relationship("User",secondary=user_reunion, back_populates="reunion")

# Table Equipe

class Equipe(Base):
    __tablename__ = 'equipe'

    id = Column(Integer, primary_key=True, index=True)
    nom_equipe = Column(String(255))

# Relation avec les membres (users)
    users = relationship("User", back_populates="equipe")

class Staff(Base):
    __tablename__ ='staff'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    telephone =Column(String(200))
    adresse = Column(String(200)) 
    user_id = Column(Integer, ForeignKey("users.id"))
    # Relation avec Membre
    users = relationship("User", back_populates="staff")
