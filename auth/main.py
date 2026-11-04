from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "eswatini_border_secret_key"
ALGORITHM = "HS256"

DATABASE_URL = "sqlite:///./auth.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    agency = Column(String)

Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str
    agency: str

@app.post("/auth/login")
def login(req: LoginRequest):
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.username == req.username).first()
    if not user:
        user = UserModel(username=req.username, password=req.password, role=req.role, agency=req.agency)
        db.add(user)
        db.commit()
    db.close()

    payload = {
        "sub": req.username,
        "role": req.role,
        "agency": req.agency,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "role": req.role, "agency": req.agency}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "auth"}
