from fastapi import FastAPI, HTTPException,Depends,status
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import  EmailStr,BaseModel
from typing import Annotated,List, Optional
import models
from models import Reunion
from models import User
from models import Equipe
from models import Staff
from schemas import UserBase, UserResponse, ReunionBase, ReunionGet,UserUpdate,EmailSchema,EquipeBase,StaffBase,StaffResponse,LoginRequest
from database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session,joinedload
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import parse_obj_as



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app=FastAPI()
SECRET_KEY = "supersecretkey"  # À protéger avec des variables d'environnement
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)



db_dependency = Annotated[Session,Depends(get_db)]


# Configuration pour les mails
conf = ConnectionConfig(
    MAIL_USERNAME="eb401f4a0a20bc",
    MAIL_PASSWORD="5ab8e0d9a462dd",
    MAIL_FROM="test21052000@gmail.com",  # Adresse de l'expéditeur
    MAIL_PORT=587,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=True,  # Utilisé pour sécuriser la connexion
    MAIL_SSL_TLS=False,  # Ne pas utiliser SSL/TLS
    USE_CREDENTIALS=True,  # Indique qu'on utilise les identifiants d'authentification
    VALIDATE_CERTS=True    # Valide le certificat SSL
)
# Route pour creer un compte
@app.post("/register")
async def register_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        # Vérifier si l'utilisateur existe déjà
        user_exists = db.query(User).filter(User.email == user.email).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

        # Créer un nouvel utilisateur
        new_user = models.User(**user.dict(exclude={"password"},exclude_unset=True))
        new_user.set_password(user.password)  # Hash et enregistre le mot de passe
           
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Recharge les données après insertion

        return {"message": "Utilisateur enregistré avec succès."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Route pour connecter un utilisateur
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(request:LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.verify_password(request.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    
    access_token = create_access_token(data={"sub": user.email, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalide.")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé.")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide.")
    
# Endpoint pour récupérer les infos de l'utilisateur connecté
@app.get("/profile")
async def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).options(
        joinedload(models.User.equipe),
        joinedload(models.User.staff),
        joinedload(models.User.reunion)  # Ajoute toutes les relations ici
    ).filter(models.User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return {user}  # FastAPI convertira l'objet SQLAlchemy en JSON automatiquement

    
@app.get("/admin/dashboard")
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs.")
    return {"message": "Bienvenue sur le tableau de bord admin."}

# Retourner tous les utilisateurs
@app.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    users = db.query(models.User).all()  # Récupérer tous les utilisateurs
    return users  # Pydantic avec orm_mode gère la conversion


# Recuperer toutes les reunions enregistrée
@app.get("/reunion",response_model=List[ReunionGet], status_code=status.HTTP_200_OK)
async def get_all_reunion(db:db_dependency):
    reunions = db.query(models.Reunion).all()  # Récupère toutes les reunions
    return reunions  # Retourne la liste des reunions


# Verification du profil 
@app.get("/user/profile-status")
def get_profile_status(current_user: User = Depends(get_current_user)):
    return {"profile_completed": current_user.profile_completed}
    
# mise a jour du profil
@app.put("/users/{user_id}/complete-profile/")
async def complete_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    user.profile_completed = True  # Marque le profil comme complété
    db.commit()
    db.refresh(user)

    return {"message": "Profil complété avec succès."}

     
@app.post("/reunion", status_code=status.HTTP_201_CREATED)
async def create_reunion(reunion: ReunionBase, db: Session = Depends(get_db)):
    # Crée un nouvel objet Reunion à partir des données reçues
    db_reunion = Reunion(**reunion.dict())

    try:
        # Ajoute la réunion à la base de données
        db.add(db_reunion)
        db.commit()  # Commit les changements
        db.refresh(db_reunion)  # Rafraîchit l'instance pour obtenir l'id généré ou d'autres champs après le commit
        
        return db_reunion  # Renvoie l'objet réunion créé, avec son id généré
    except Exception as e:
        db.rollback()  # En cas d'erreur, annule la transaction
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout de la réunion : {str(e)}")      
        
     
    
    


@app.post("/send_mail")
async def send_mail(email: EmailSchema):
    if not isinstance(email.email, list) or not email.email:
        return JSONResponse(status_code=422, content={"message": "Email list is missing or not correctly formatted."})

    template = """
        <html>
        <body>
        <p>Hi !!!<br>Merci de m'avoir donné ton mail pour le test</p>
        </body>
        </html>
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.email,  # Récupère directement la liste des destinataires
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)

    return JSONResponse(status_code=200, content={"message": "Email has been sent"})


# Recuperer un utilisateur a partir de son id
@app.get("/user/{id}", status_code=status.HTTP_200_OK)
async def read_user(id:int, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.id ==id).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail='Utilisateur introuvable')
    return db_user

# Recuperer une reunion a partir de  son id 
@app.get("/reunion/{id}",status_code=status.HTTP_200_OK)
async def read_reunion(id:int,db:db_dependency):
    db_reunion = db.query(models.Reunion).filter(models.Reunion.id == id).first()
    if db_reunion is None:
        raise HTTPException(status_code=404, detail='Réunion introuvable')
    return db_reunion


# Fonction pour effectué la suppression d'un utilisateur depuis la base  de données
@app.delete("/user/{id}", status_code = status.HTTP_200_OK)
async def delete_user(id:int, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.id ==id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Utilisateur introuvable')
    db.delete(db_user)
    db.commit()
    
 # Mise à jour de l'utilisateur 


@app.put("/user/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, user: UserBase, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == id).first()  # Récupérer l'utilisateur existant
    if db_user is None:
        raise HTTPException(status_code=404, detail='Utilisateur introuvable')
    
    # Mettre à jour les attributs de l'utilisateur
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    
    db.commit()  # Enregistrer les modifications
    return db_user  # Retourner l'utilisateur mis à jour


# Route PATCH pour mettre à jour partiellement un utilisateur
@app.patch("/user/{id}", response_model=UserBase, status_code=status.HTTP_200_OK)
async def update_user_partial(id: int, user_update: UserUpdate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == id).first()  # Récupérer l'utilisateur existant
    if db_user is None:
        raise HTTPException(status_code=404, detail='Utilisateur introuvable')

    # Mettre à jour uniquement les champs fournis
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()  # Enregistrer les modifications
    return db_user  # Retourner l'utilisateur mis à jour



# Route post pour créer une équipe

@app.post("/equipe",  status_code=status.HTTP_201_CREATED)
async def create_equipe(equipe: EquipeBase, db: Session = Depends(get_db)):
    # Crée un nouvel objet equipe à partir des données reçues
    db_equipe = Equipe(**equipe.dict())
    
    try:
        # Ajoute l'equipe à la base de données
        db.add(db_equipe)
        db.commit()  # Commit les changements
        db.refresh(db_equipe)  # Rafraîchit l'instance pour obtenir l'id généré ou d'autres champs après le commit
        
        return db_equipe  # Renvoie l'objet equipe créé, avec son id généré
    except Exception as e:
        db.rollback()  # En cas d'erreur, annule la transaction
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout de l'equipe : {str(e)}")    


# Route pour ajouter des utilisateurs dans une equipe

@app.post("/equipe/{id}/users", status_code=status.HTTP_201_CREATED)
async def add_users_to_equipe(id: int, users: List[int], db: Session = Depends(get_db)):
    equipe = db.query(Equipe).filter(Equipe.id == id).first()
    
    if not equipe:
        raise HTTPException(status_code=404, detail="Équipe introuvable")
    
    # Vérifier les utilisateurs et éviter les doublons
    valid_users = db.query(User).filter(User.id.in_(users)).all()
    
    if len(valid_users) != len(users):
        raise HTTPException(status_code=400, detail="Un ou plusieurs utilisateurs sont introuvables")

    # Vérifier combien d'utilisateurs sont déjà dans l'équipe
    existing_users = db.query(User).filter(User.equipe_id == id).count()

    if existing_users + len(users) > 5:
        raise HTTPException(status_code=400, detail="Une équipe ne peut pas avoir plus de 5 membres")

    # Liste des rôles disponibles
    roles = ["Responsable d'équipe", "Secrétaire d'équipe", "Adjoint", "Membre", "Membre"]
    
    for i, user in enumerate(valid_users):
        user.equipe_id = id
        user.role = roles[existing_users + i]  # Assigner les rôles par ordre
        db.add(user)

    db.commit()

    return {"message": "Utilisateurs ajoutés avec succès", "equipe_id": id}


# Route pour recuperer les utilisateurs d'une equipe

@app.get("/equipe/{id}/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users_in_equipe(id: int, db: Session = Depends(get_db)):
    # Récupérer l'équipe
    equipe = db.query(Equipe).filter(Equipe.id == id).first()

    if equipe is None:
        raise HTTPException(status_code=404, detail="Équipe introuvable")

    # Récupérer les utilisateurs associés à cette équipe
    users_in_equipe = db.query(User).filter(User.equipe_id == id).all()

    return users_in_equipe
# ajouter un staff pour un user specifique
@app.post("/staff/{user_id}", status_code=201)
async def create_staff(user_id: int, staff: StaffBase, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Création du staff et association avec l'utilisateur
    db_staff = Staff(**staff.dict(), user_id=user_id)

    try:
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        return db_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout du staff : {str(e)}")
    
# Recuperer les staffs d'un utilisateur
@app.get("/user/{user_id}/staff", response_model=List[StaffResponse], status_code=200)
async def get_staff(user_id: int, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupère les staffs associés à cet utilisateur
    staffs = db.query(Staff).filter(Staff.user_id == user_id).all()

    return staffs


