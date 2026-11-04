from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Port Health Service (Ministry of Health)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./health.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScreeningModel(Base):
    __tablename__ = "screenings"
    travellerId = Column(String, primary_key=True, index=True)
    temperature = Column(Float)
    hasSymptoms = Column(String)
    vaccinationStatus = Column(String)
    result = Column(String)

Base.metadata.create_all(bind=engine)

class HealthScreening(BaseModel):
    travellerId: str
    temperature: float
    hasSymptoms: bool
    vaccinationStatus: str

@app.post("/screenings", status_code=201)
def record_screening(screening: HealthScreening):
    db = SessionLocal()
    result = "QUARANTINE_REQUIRED" if screening.temperature > 38.0 or screening.hasSymptoms else "PASSED"
    status = "HOLD" if result == "QUARANTINE_REQUIRED" else "APPROVED"
    
    existing = db.query(ScreeningModel).filter(ScreeningModel.travellerId == screening.travellerId).first()
    if existing:
        existing.temperature = screening.temperature
        existing.hasSymptoms = str(screening.hasSymptoms)
        existing.vaccinationStatus = screening.vaccinationStatus
        existing.result = result
    else:
        db_screening = ScreeningModel(
            travellerId=screening.travellerId,
            temperature=screening.temperature,
            hasSymptoms=str(screening.hasSymptoms),
            vaccinationStatus=screening.vaccinationStatus,
            result=result
        )
        db.add(db_screening)
    db.commit()
    db.close()
    return {"travellerId": screening.travellerId, "result": result, "status": status}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "port_health"}
