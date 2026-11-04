from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Environment Service (Tourism & Environment)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./environment.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PermitModel(Base):
    __tablename__ = "permits"
    permitNumber = Column(String, primary_key=True, index=True)
    speciesOrProduct = Column(String)
    quantity = Column(Integer)
    validityStatus = Column(String)

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    if not db.query(PermitModel).first():
        db.add(PermitModel(permitNumber="CITES-2026-001", speciesOrProduct="Flora Sample", quantity=10, validityStatus="VALID"))
        db.add(PermitModel(permitNumber="CITES-EXPIRED", speciesOrProduct="Timber", quantity=100, validityStatus="EXPIRED"))
        db.commit()
    db.close()

seed()

@app.get("/permits/{permit_number}/validity")
def validate_permit(permit_number: str):
    db = SessionLocal()
    permit = db.query(PermitModel).filter(PermitModel.permitNumber == permit_number).first()
    db.close()
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    is_valid = permit.validityStatus == "VALID"
    return {
        "permitNumber": permit_number,
        "isValid": is_valid,
        "status": "APPROVED" if is_valid else "REJECTED"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "environment"}
