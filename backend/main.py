from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, auth, predictions
from app.database import engine, Base
import os
from app.routers import auth, students, predictions

# Import models
from app.models import User, Student

# Create all tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartScholar API",
    description="AI-powered academic success platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "SmartScholar API is running!", "version": "1.0.0"}

# Health check - UPDATED
@app.get("/health")
def health_check():
    # Check which database is being used
    db_url = os.getenv("DATABASE_URL", "")
    db_type = "SQLite" if "sqlite" in db_url else "PostgreSQL"
    
    return {
        "status": "healthy",
        "database": f"{db_type} connected",
        "database_file": "smartscholar.db" if db_type == "SQLite" else "cloud"
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])