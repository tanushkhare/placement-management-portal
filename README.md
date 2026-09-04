# ⚡ Placement Management Portal

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://placement-management-portal-web.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://placement-management-portal-web.vercel.app](https://placement-management-portal-web.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Relational candidate eligibility and placement screening engine built on SQLAlchemy declarative models and transactional database session dependencies.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** SQLAlchemy, SQLite / PostgreSQL, FastAPI, Pydantic
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Persistent Relational Layer:** Replaced volatile in-memory dicts with SQLAlchemy declarative models.
* **Session Dependency Injection:** Prevents database connection leaks via generator sessions.
* **CORS Origin Protection:** Restricts API consumption to trusted frontend domains.

---

## 🚀 API Contracts
```http
POST /api/v1/students/screen
Request:
{
  "cgpa": 8.4,
  "backlogs": 0,
  "specialization": "Systems"
}

Response (200 OK):
{
  "eligible": true,
  "matched_count": 4,
  "postings": [
    {"company": "Google", "role": "Cloud Systems Engineer", "cutoff": 8.0},
    {"company": "Stripe", "role": "Distributed Infrastructure", "cutoff": 8.2}
  ]
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v