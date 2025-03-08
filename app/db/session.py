from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings  # Importe les paramètres de configuration

# Crée un moteur de base de données en utilisant l'URL de la base de données depuis les variables d'environnement
engine = create_engine(settings.database_url)

# Crée une fabrique de sessions pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Dépendance pour obtenir une session de base de données
def get_db():
    """
    Fournit une session de base de données pour chaque requête.
    La session est automatiquement fermée après utilisation.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()