from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import re
from typing import Optional
from app.database.mongodb import Database

app = FastAPI()

class ComplaintCreate(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone_number": "1234567890",
                "email": "johndoe@example.com",
                "complaint_details": "My order #12345 was supposed to arrive on May 1 but is still not here."
            }
        }

class ComplaintResponse(BaseModel):
    complaint_id: str
    message: str = "Complaint created successfully"

def get_db():
    return Database()

def validate_phone_number(phone_number: str) -> bool:
    return bool(re.match(r'^\d{10,15}$', phone_number))

@app.post("/complaints", response_model=ComplaintResponse, tags=["Complaints"])
async def create_complaint(complaint: ComplaintCreate, db: Database = Depends(get_db)):
    if not validate_phone_number(complaint.phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    complaint_id = db.create_complaint(
        name=complaint.name,
        phone_number=complaint.phone_number,
        email=complaint.email,
        complaint_details=complaint.complaint_details
    )
    return {"complaint_id": complaint_id}

@app.get("/complaints/{complaint_id}", tags=["Complaints"])
async def get_complaint(complaint_id: str, db: Database = Depends(get_db)):
    complaint = db.get_complaint(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint["_id"] = str(complaint["_id"])
    complaint["created_at"] = complaint["created_at"].isoformat()
    return complaint
