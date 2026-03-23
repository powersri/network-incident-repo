# main.py - FastAPI backend for network incident reporting
from fastapi import FastAPI
# fastapi imports for CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Local imports for routers and database
from auth import router as auth_router
# Import the incidents router
from incidents import router as incidents_router

# Initialize FastAPI app
app = FastAPI(
    title="Network Incident Reporting API", # Updated title for better clarity
    version="1.0.0", # Added versioning for better API management
    description="Production-ready FastAPI backend for network incident reporting" # Updated description to reflect production readiness
)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Update these origins to match your frontend development URLs
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://network-incident-repo.onrender.com/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for authentication and incidents
app.include_router(auth_router)
app.include_router(incidents_router)

# Health check endpoint to verify API is running
@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }