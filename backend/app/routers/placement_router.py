from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import uuid

router = APIRouter(prefix="/api/v1/placement", tags=["Placement Portal"])

class DriveApplicationRequest(BaseModel):
    student_name: str = Field(..., min_length=2)
    student_id: str = Field(..., min_length=3)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    target_role: str
    skills: List[str]

class DriveEvaluationResponse(BaseModel):
    application_id: str
    student_name: str
    eligibility_status: str
    match_score: float
    shortlist_status: str
    scheduled_round: str
    criteria_feedback: List[str]

@router.post("/evaluate", response_model=DriveEvaluationResponse)
async def evaluate_drive_application(payload: DriveApplicationRequest):
    min_cgpa_cutoff = 7.5
    priority_skills = {"python", "fastapi", "docker", "sql", "aws", "react", "c++", "data structures"}
    
    normalized_skills = {s.lower().strip() for s in payload.skills}
    matched = priority_skills.intersection(normalized_skills)
    skill_score = (len(matched) / max(len(priority_skills), 1)) * 100
    
    is_eligible = payload.cgpa >= min_cgpa_cutoff
    match_score = round((payload.cgpa / 10.0 * 50) + (min(skill_score, 100) * 0.5), 1)
    
    feedback = []
    if is_eligible:
        feedback.append(f"Academic benchmark satisfied (CGPA {payload.cgpa} >= {min_cgpa_cutoff})")
    else:
        feedback.append(f"Below CGPA cutoff benchmark ({payload.cgpa} < {min_cgpa_cutoff})")
        
    if matched:
        feedback.append(f"Matched core competencies: {', '.join(sorted([m.title() for m in matched]))}")
    else:
        feedback.append("No primary role competencies matched in candidate profile.")

    shortlisted = is_eligible and match_score >= 65.0
    scheduled_round = "Technical Assessment & System Design" if shortlisted else "Profile On Hold / Additional Review"

    return DriveEvaluationResponse(
        application_id=f"APP-{uuid.uuid4().hex[:8].upper()}",
        student_name=payload.student_name,
        eligibility_status="ELIGIBLE" if is_eligible else "INELIGIBLE",
        match_score=match_score,
        shortlist_status="SHORTLISTED FOR INTERVIEW" if shortlisted else "NOT SHORTLISTED",
        scheduled_round=scheduled_round,
        criteria_feedback=feedback
    )
