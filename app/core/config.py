from pydantic_settings import BaseSettings  # Utilise pydantic-settings au lieu de pydantic

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str  # Exemple de variable d'environnement

    class Config:
        env_file = ".env"  # Charge les variables depuis un fichier .env

# Crée une instance de Settings
settings = Settings()