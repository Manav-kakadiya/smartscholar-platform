from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.auth import get_current_user
import joblib
import json
import numpy as np
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Load models
try:
    dropout_model = joblib.load('app/ml/dropout_model.pkl')
    dropout_scaler = joblib.load('app/ml/dropout_scaler.pkl')
    with open('app/ml/dropout_features.json', 'r') as f:
        dropout_features = json.load(f)
    
    gpa_model = joblib.load('app/ml/gpa_model.pkl')
    gpa_scaler = joblib.load('app/ml/gpa_scaler.pkl')
    with open('app/ml/gpa_features.json', 'r') as f:
        gpa_features = json.load(f)
    
    models_loaded = True
except:
    models_loaded = False
    print("⚠️ ML models not loaded. Train models first!")

class PredictionInput(BaseModel):
    age: int = 20
    previous_gpa: float = 3.0
    current_gpa: float = 3.0
    attendance_rate: float = 85.0
    assignment_completion: float = 80.0
    study_hours_per_week: int = 15
    forum_posts: int = 10
    days_since_last_login: int = 2
    financial_aid: int = 0
    part_time_job: int = 0
    commute_time: int = 30

class PredictionResponse(BaseModel):
    dropout_risk: int
    dropout_probability: float
    predicted_gpa: float
    risk_level: str
    recommendations: List[str]

@router.post("/predict", response_model=PredictionResponse)
async def predict_student_outcome(
    data: PredictionInput,
    current_user: dict = Depends(get_current_user)
):
    if not models_loaded:
        raise HTTPException(status_code=503, detail="ML models not available")
    
    # Prepare dropout prediction data
    dropout_input = [
        data.age,
        data.previous_gpa,
        data.current_gpa,
        data.attendance_rate,
        data.assignment_completion,
        data.study_hours_per_week,
        data.forum_posts,
        data.days_since_last_login,
        data.financial_aid,
        data.part_time_job,
        data.commute_time
    ]
    
    # Prepare GPA prediction data
    gpa_input = [
        data.age,
        data.previous_gpa,
        data.current_gpa,
        data.attendance_rate,
        data.assignment_completion,
        data.study_hours_per_week,
        data.forum_posts,
        data.days_since_last_login
    ]
    
    # Make predictions
    dropout_input_scaled = dropout_scaler.transform([dropout_input])
    dropout_prob = dropout_model.predict_proba(dropout_input_scaled)[0][1]
    dropout_risk = int(dropout_prob * 100)
    
    gpa_input_scaled = gpa_scaler.transform([gpa_input])
    predicted_gpa = float(gpa_model.predict(gpa_input_scaled)[0])
    predicted_gpa = round(max(0, min(4.0, predicted_gpa)), 2)
    
    # Determine risk level
    if dropout_risk > 60:
        risk_level = "high"
    elif dropout_risk > 30:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # Generate recommendations
    recommendations = []
    if data.attendance_rate < 70:
        recommendations.append("⚠️ Improve attendance - aim for at least 85%")
    if data.assignment_completion < 70:
        recommendations.append("📝 Complete more assignments on time")
    if data.days_since_last_login > 5:
        recommendations.append("🔔 Log in more frequently to stay engaged")
    if data.study_hours_per_week < 12:
        recommendations.append("📚 Increase study time - aim for 15+ hours/week")
    if predicted_gpa < data.current_gpa:
        recommendations.append("📉 Your performance may decline - seek help early")
    
    if not recommendations:
        recommendations.append("✅ Keep up the good work!")
    
    return {
        "dropout_risk": dropout_risk,
        "dropout_probability": round(dropout_prob, 3),
        "predicted_gpa": predicted_gpa,
        "risk_level": risk_level,
        "recommendations": recommendations
    }

class AssignmentText(BaseModel):
    text: str

@router.post("/analyze-assignment")
async def analyze_assignment_endpoint(
    assignment: AssignmentText,
    current_user: dict = Depends(get_current_user)
):
    from app.ml.assignment_feedback import analyze_assignment
    
    result = analyze_assignment(assignment.text)
    return result