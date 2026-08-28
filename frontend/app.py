import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Placement Management Portal", layout="wide")

st.title("🎓 Enterprise Placement Management & Career Portal")
st.markdown("Automated CGPA screening, skill taxonomy matching, and enterprise recruitment pipeline management.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Candidate Application Desk")
    student_id = st.selectbox("Select Registered Candidate", ["SRM_CS_01 (Tanush Khare - 9.2 CGPA)", "SRM_CS_02 (Marcus Vance - 7.8 CGPA)"])
    s_id = "SRM_CS_01" if "SRM_CS_01" in student_id else "SRM_CS_02"
    company = st.selectbox("Target Enterprise", ["Google", "Microsoft", "Amazon", "NVIDIA", "Uber"])
    min_cgpa = st.slider("Minimum CGPA Cutoff Threshold", 6.0, 9.5, 8.5, step=0.1)

    if st.button("Submit Placement Application", type="primary"):
        with st.spinner("Screening academic eligibility and indexing skill vectors..."):
            try:
                res = requests.post(
                    "http://localhost:8000/api/v1/placement/apply",
                    json={"student_id": s_id, "target_company": company, "min_cgpa_cutoff": min_cgpa},
                    timeout=5
                )
                if res.status_code == 200:
                    st.session_state["p07_result"] = res.json()
                    st.success("Application Processed Successfully!")
                else:
                    st.error(f"Application Error: {res.text}")
            except Exception:
                st.warning("Backend offline. Simulating recruitment validation.")
                is_pass = s_id == "SRM_CS_01" and 9.2 >= min_cgpa
                st.session_state["p07_result"] = {
                    "application_id": "APP-SIM9001",
                    "student_id": s_id,
                    "full_name": "Tanush Khare" if s_id == "SRM_CS_01" else "Marcus Vance",
                    "target_company": company,
                    "cgpa": 9.2 if s_id == "SRM_CS_01" else 7.8,
                    "eligibility_status": "SHORTLISTED_FOR_INTERVIEW" if is_pass else "CGPA_CRITERIA_UNMET",
                    "skill_match_pct": 83.3 if s_id == "SRM_CS_01" else 50.0,
                    "timestamp": "2026-08-28T10:45:00Z"
                }

with col2:
    if "p07_result" in st.session_state:
        res = st.session_state["p07_result"]
        st.subheader(f"Application Record: {res['application_id']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Candidate", res["full_name"])
        m2.metric("CGPA", res["cgpa"])
        m3.metric("Skill Match", f"{res['skill_match_pct']}%")
        
        if "SHORTLISTED" in res["eligibility_status"]:
            st.success(f"🎉 Eligible for **{res['target_company']}**: Candidate meets academic threshold.")
        else:
            st.error(f"❌ Application Screened Out: Minimum cutoff ({min_cgpa}) exceeded candidate CGPA.")
            
        st.markdown(f"**Application Timestamp:** `{res['timestamp']}`")
