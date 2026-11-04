from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Customs Service (ERS)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./customs.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DeclarationModel(Base):
    __tablename__ = "declarations"
    declarationNumber = Column(String, primary_key=True, index=True)
    kind = Column(String)
    agent = Column(String)
    vehicleReg = Column(String, nullable=True)
    items = Column(JSON)

Base.metadata.create_all(bind=engine)

class DeclarationItem(BaseModel):
    description: str
    tariffCode: str
    quantity: int
    value: float
    regulated: bool = False

class DeclarationCreate(BaseModel):
    declarationNumber: str
    kind: str
    agent: str
    vehicleReg: Optional[str] = None
    items: List[DeclarationItem]

@app.post("/declarations", status_code=201)
def submit_declaration(dec: DeclarationCreate):
    db = SessionLocal()
    existing = db.query(DeclarationModel).filter(DeclarationModel.declarationNumber == dec.declarationNumber).first()
    if existing:
        db.close()
        raise HTTPException(status_code=409, detail="Declaration already exists")
    db_dec = DeclarationModel(
        declarationNumber=dec.declarationNumber,
        kind=dec.kind,
        agent=dec.agent,
        vehicleReg=dec.vehicleReg,
        items=[item.dict() for item in dec.items]
    )
    db.add(db_dec)
    db.commit()
    db.close()
    return {"message": "Declaration submitted successfully", "declarationNumber": dec.declarationNumber}

@app.get("/declarations/{declaration_number}")
def get_declaration(declaration_number: str):
    db = SessionLocal()
    dec = db.query(DeclarationModel).filter(DeclarationModel.declarationNumber == declaration_number).first()
    db.close()
    if not dec:
        raise HTTPException(status_code=404, detail="Declaration not found")
    return {
        "declarationNumber": dec.declarationNumber,
        "kind": dec.kind,
        "agent": dec.agent,
        "vehicleReg": dec.vehicleReg,
        "items": dec.items
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "customs"}
