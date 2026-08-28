from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.schemas.placement_schema import StudentRegistration, JobApplicationRequest, ApplicationRecord
from backend.app.services.placement_service import placement_engine

router = APIRouter(prefix="/api/v1/placement", tags=["Placement Management Portal"])

@router.post("/register")
async def register_student(payload: StudentRegistration):
    return placement_engine.register_student(
        payload.student_id, payload.full_name, payload.cgpa, payload.department, payload.primary_skills
    )

@router.post("/apply", response_model=ApplicationRecord)
async def submit_application(payload: JobApplicationRequest):
    try:
        record = placement_engine.process_application(payload.student_id, payload.target_company, payload.min_cgpa_cutoff)
        return ApplicationRecord(**record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/applications", response_model=List[ApplicationRecord])
async def list_applications():
    return placement_engine.applications
