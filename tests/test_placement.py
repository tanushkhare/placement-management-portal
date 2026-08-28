import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_eligible_student_application():
    payload = {
        "student_id": "SRM_CS_01",
        "target_company": "Google",
        "min_cgpa_cutoff": 8.5
    }
    res = client.post("/api/v1/placement/apply", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "APP-" in data["application_id"]
    assert data["eligibility_status"] == "SHORTLISTED_FOR_INTERVIEW"
    assert data["cgpa"] == 9.2

def test_ineligible_student_application():
    payload = {
        "student_id": "SRM_CS_02",
        "target_company": "Google",
        "min_cgpa_cutoff": 8.5
    }
    res = client.post("/api/v1/placement/apply", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["eligibility_status"] == "CGPA_CRITERIA_UNMET"
