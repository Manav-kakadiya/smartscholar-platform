from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, auth, predictions

app = FastAPI(
    title="SmartScholar API",
    description="AI-powered academic success platform",
    version="1.0.0"
)

# Enable CORS for frontend
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
    return {"message": "SmartScholar API is running!"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routers (empty for now, will add routes in Phase 3)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)