from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import placement_router
import uvicorn

app = FastAPI(
    title="Placement Management & Student Career Portal API",
    description="Student registry, eligibility screening, and enterprise recruitment tracking backend.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(placement_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "placement-management-portal"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
