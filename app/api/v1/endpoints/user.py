from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from typing import List,Optional,Dict
from app.schemas.user import UserBase, UserResponse, UserUpdate
from app.schemas.login import LoginRequest
from app.models.user import User
from app.db.session import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
# Configuration pour les tokens JWT
SECRET_KEY = "supersecretkey"  # À protéger avec des variables d'environnement
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()

# Configuration pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crée un token JWT pour un utilisateur
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



@router.post("/register", response_model=UserResponse)
async def register_user(user: UserBase, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe déjà
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Hash le mot de passe avant de l'enregistrer
    hashed_password = pwd_context.hash(user.password)

    # Crée un nouvel utilisateur
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password_hash=hashed_password,  # Utilise password_hash au lieu de password
        is_admin=user.is_admin,
        role=user.role,
        conduite=user.conduite,
        profile_completed=user.profile_completed
    )

    # Ajoute l'utilisateur à la base de données
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    # Crée un token JWT
    access_token = create_access_token(data={"sub": user.email, "is_admin": user.is_admin})

    return {"access_token": access_token,"is_admin":user.is_admin,   "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# recupère tous les utilisateurs
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Recupère un utilisateur par ID
@router.get("/user/{id}", response_model=UserResponse)
async def read_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mettre à jour un utilisateur par ID
@router.put("/user/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Met à jour les champs de l'utilisateur
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

# Supprime un utilisateur par ID
@router.delete("/user/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
   try:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        db.delete(user)
        db.commit()
        return {"detail": "Utilisateur supprimé"}
   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Recuperation de profil utilisateur
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).options(
        joinedload(User.equipe),
        joinedload(User.staff),
        joinedload(User.reunion)  # Ajoute toutes les relations ici
    ).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return {user}  # FastAPI convertira l'objet SQLAlchemy en JSON automatiquement
