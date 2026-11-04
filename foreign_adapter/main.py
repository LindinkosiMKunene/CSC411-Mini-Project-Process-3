from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Foreign Agency Adapter (SARS / Mozambique)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoticePayload(BaseModel):
    caseNumber: str
    noticeType: str
    destinationCountry: str

@app.post("/notices")
def send_notice(notice: NoticePayload):
    return {
        "status": "SENT",
        "caseNumber": notice.caseNumber,
        "destination": notice.destinationCountry,
        "message": "Notice dispatched to foreign agency gateway"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "foreign_adapter"}
