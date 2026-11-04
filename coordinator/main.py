from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Coordinator Service (Hub)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./coordinator.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CaseModel(Base):
    __tablename__ = "cases"
    caseNumber = Column(String, primary_key=True, index=True)
    post = Column(String)
    direction = Column(String)
    caseType = Column(String)
    travellerId = Column(String, nullable=True)
    declarationNumber = Column(String, nullable=True)
    clearances = Column(JSON)
    status = Column(String)

Base.metadata.create_all(bind=engine)

class CrossingCaseCreate(BaseModel):
    caseNumber: str
    post: str
    direction: str
    caseType: str = "PERSON"
    travellerId: Optional[str] = None
    declarationNumber: Optional[str] = None

class ClearanceUpdate(BaseModel):
    state: str
    reasonCode: Optional[str] = None
    decidedBy: str

def evaluate_release_rule(clearances: dict) -> str:
    states = [c["state"] for c in clearances.values()]
    if "REJECTED" in states:
        return "REFUSED"
    if "HOLD" in states:
        return "ON_HOLD"
    if all(s == "APPROVED" for s in states if s != "NOT_REQUIRED"):
        return "CLEARED"
    return "IN_PROGRESS"

@app.post("/cases", status_code=201)
def create_case(case: CrossingCaseCreate):
    db = SessionLocal()
    existing = db.query(CaseModel).filter(CaseModel.caseNumber == case.caseNumber).first()
    if existing:
        db.close()
        raise HTTPException(status_code=409, detail="Case already exists")
    
    clearances = {}
    if case.travellerId:
        clearances["immigration"] = {"state": "PENDING", "reasonCode": None, "decidedBy": None}
    if case.declarationNumber:
        clearances["customs"] = {"state": "PENDING", "reasonCode": None, "decidedBy": None}
        clearances["environment"] = {"state": "PENDING", "reasonCode": None, "decidedBy": None}
    if case.caseType in ["PERSON", "BOTH"]:
        clearances["health"] = {"state": "PENDING", "reasonCode": None, "decidedBy": None}

    db_case = CaseModel(
        caseNumber=case.caseNumber,
        post=case.post,
        direction=case.direction,
        caseType=case.caseType,
        travellerId=case.travellerId,
        declarationNumber=case.declarationNumber,
        clearances=clearances,
        status="IN_PROGRESS"
    )
    db.add(db_case)
    db.commit()
    db.close()
    return {"message": "Crossing case opened", "caseNumber": case.caseNumber, "status": "IN_PROGRESS"}

@app.get("/cases/{case_number}")
def get_case(case_number: str):
    db = SessionLocal()
    case = db.query(CaseModel).filter(CaseModel.caseNumber == case_number).first()
    db.close()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {
        "caseNumber": case.caseNumber,
        "post": case.post,
        "direction": case.direction,
        "caseType": case.caseType,
        "travellerId": case.travellerId,
        "declarationNumber": case.declarationNumber,
        "clearances": case.clearances,
        "status": case.status
    }

@app.get("/cases")
def list_cases():
    db = SessionLocal()
    cases = db.query(CaseModel).all()
    db.close()
    return [{
        "caseNumber": c.caseNumber,
        "post": c.post,
        "direction": c.direction,
        "status": c.status,
        "clearances": c.clearances
    } for c in cases]

@app.put("/cases/{case_number}/clearances/{agency}")
def update_clearance(case_number: str, agency: str, update: ClearanceUpdate):
    db = SessionLocal()
    case = db.query(CaseModel).filter(CaseModel.caseNumber == case_number).first()
    if not case:
        db.close()
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Create a clean dictionary copy of clearances
    clearances = dict(case.clearances) if case.clearances else {}
    if agency not in clearances:
        db.close()
        raise HTTPException(status_code=400, detail=f"Agency '{agency}' is not required for this case")
    
    clearances[agency] = {
        "state": update.state,
        "reasonCode": update.reasonCode,
        "decidedBy": update.decidedBy
    }
    
    case.clearances = clearances
    case.status = evaluate_release_rule(clearances)
    
    db.commit()
    
    # Extract values into local variables while attached to the session
    res_case_number = case.caseNumber
    res_status = case.status
    res_clearances = case.clearances
    
    db.close()
    
    # Return plain dictionary to prevent detached instance serialization errors
    return {
        "caseNumber": res_case_number,
        "overallStatus": res_status,
        "clearances": res_clearances
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "coordinator"}
