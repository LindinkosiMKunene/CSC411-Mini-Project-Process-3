from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Immigration Service (Home Affairs)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./immigration.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TravellerModel(Base):
    __tablename__ = "travellers"
    travellerId = Column(String, primary_key=True, index=True)
    fullName = Column(String)
    nationality = Column(String)
    dateOfBirth = Column(String)
    passportNumber = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

class TravellerCreate(BaseModel):
    travellerId: str
    fullName: str
    nationality: str
    dateOfBirth: str
    passportNumber: str

@app.post("/travellers", status_code=201)
def register_traveller(traveller: TravellerCreate):
    db = SessionLocal()
    existing = db.query(TravellerModel).filter(TravellerModel.travellerId == traveller.travellerId).first()
    if existing:
        db.close()
        raise HTTPException(status_code=409, detail="Traveller already registered")
    db_traveller = TravellerModel(**traveller.dict())
    db.add(db_traveller)
    db.commit()
    db.close()
    return {"message": "Traveller registered successfully", "travellerId": traveller.travellerId}

@app.get("/travellers/{traveller_id}")
def get_traveller(traveller_id: str):
    db = SessionLocal()
    traveller = db.query(TravellerModel).filter(TravellerModel.travellerId == traveller_id).first()
    db.close()
    if not traveller:
        raise HTTPException(status_code=404, detail="Traveller not found")
    return {
        "travellerId": traveller.travellerId,
        "fullName": traveller.fullName,
        "nationality": traveller.nationality,
        "dateOfBirth": traveller.dateOfBirth,
        "passportNumber": traveller.passportNumber
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "immigration"}
