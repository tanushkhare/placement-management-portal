import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

class PlacementManagementEngine:
    def __init__(self):
        self.students: Dict[str, Dict[str, Any]] = {
            "SRM_CS_01": {
                "student_id": "SRM_CS_01",
                "full_name": "Tanush Khare",
                "cgpa": 9.2,
                "department": "Computer Science & Engineering",
                "primary_skills": ["Python", "FastAPI", "Docker", "Machine Learning", "Distributed Systems"]
            },
            "SRM_CS_02": {
                "student_id": "SRM_CS_02",
                "full_name": "Marcus Vance",
                "cgpa": 7.8,
                "department": "Information Technology",
                "primary_skills": ["Java", "SQL", "HTML/CSS"]
            }
        }
        self.applications: List[Dict[str, Any]] = []

    def register_student(self, s_id: str, name: str, cgpa: float, dept: str, skills: List[str]) -> Dict[str, Any]:
        self.students[s_id] = {
            "student_id": s_id,
            "full_name": name,
            "cgpa": cgpa,
            "department": dept,
            "primary_skills": skills
        }
        return {"status": "SUCCESS", "student_id": s_id, "full_name": name}

    def process_application(self, s_id: str, company: str, cutoff: float) -> Dict[str, Any]:
        student = self.students.get(s_id)
        if not student:
            raise ValueError(f"Student record '{s_id}' not found in registry database.")

        is_eligible = student["cgpa"] >= cutoff
        status = "SHORTLISTED_FOR_INTERVIEW" if is_eligible else "CGPA_CRITERIA_UNMET"
        
        # Skill-match evaluation
        core_keywords = ["Python", "FastAPI", "Distributed Systems", "SQL", "Docker", "Machine Learning"]
        matched_skills = [s for s in student["primary_skills"] if s in core_keywords]
        match_pct = round((len(matched_skills) / len(core_keywords)) * 100, 1)

        record = {
            "application_id": f"APP-{uuid.uuid4().hex[:8].upper()}",
            "student_id": s_id,
            "full_name": student["full_name"],
            "target_company": company,
            "cgpa": student["cgpa"],
            "eligibility_status": status,
            "skill_match_pct": match_pct,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.applications.append(record)
        return record

placement_engine = PlacementManagementEngine()
