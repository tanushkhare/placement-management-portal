from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Placement Management Portal API")

class StudentApplication(BaseModel):
    student_name: str
    company_name: str
    role: str
    cgpa: float

applications_db = []

@app.post("/api/applications", response_model=StudentApplication)
def create_application(application: StudentApplication):
    applications_db.append(application)
    return application

@app.get("/api/applications", response_model=List[StudentApplication])
def get_applications():
    return applications_db

@app.get("/")
def read_root():
    return {"message": "Placement Management Portal Backend is running successfully!"}