from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user, reunion, staff, cours, equipe, points
from app.db.session import SessionLocal, get_db,Base,engine
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(reunion.router, prefix="/api/v1", tags=["reunions"])
app.include_router(staff.router, prefix="/api/v1", tags=["staff"])
app.include_router(cours.router, prefix="/api/v1", tags=["cours"])
app.include_router(equipe.router, prefix="/api/v1", tags=["equipe"])
app.include_router(points.router, prefix="/api/v1", tags=["points"])

@app.on_event("startup")
async def startup():
    # Créer les tables de la base de données
    Base.metadata.create_all(bind=engine)