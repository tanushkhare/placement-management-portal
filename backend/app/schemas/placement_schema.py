from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class StudentRegistration(BaseModel):
    student_id: str = Field(..., description="University Roll / Student ID (e.g. SRM_2026_CS01)")
    full_name: str = Field(..., min_length=2)
    cgpa: float = Field(..., ge=0.0, le=10.0, description="Cumulative Grade Point Average")
    department: str = Field(default="Computer Science & Engineering")
    primary_skills: List[str] = Field(..., min_length=1)

class JobApplicationRequest(BaseModel):
    student_id: str
    target_company: str = Field(..., description="Recruiting Enterprise (e.g. Google, Microsoft, Amazon)")
    min_cgpa_cutoff: float = Field(default=8.0, ge=0.0, le=10.0)

class ApplicationRecord(BaseModel):
    application_id: str
    student_id: str
    full_name: str
    target_company: str
    cgpa: float
    eligibility_status: str
    skill_match_pct: float
    timestamp: str
