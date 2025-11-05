from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.auth import get_current_user
from typing import List
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class StudentResponse(BaseModel):
    id: str
    name: str
    email: str
    student_id: str
    gpa: float
    risk_score: int
    risk_level: str

    class Config:
        from_attributes = True

@router.get("/me", response_model=StudentResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    return {
        "id": str(student.id),
        "name": user.name,
        "email": user.email,
        "student_id": student.student_id,
        "gpa": float(student.gpa),
        "risk_score": student.risk_score,
        "risk_level": student.risk_level
    }

@router.get("/all", response_model=List[StudentResponse])
async def get_all_students(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only advisors can view all students
    if current_user.get("user_type") != "advisor":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    students = db.query(Student, User).join(User, Student.user_id == User.id).all()
    
    result = []
    for student, user in students:
        result.append({
            "id": str(student.id),
            "name": user.name,
            "email": user.email,
            "student_id": student.student_id,
            "gpa": float(student.gpa),
            "risk_score": student.risk_score,
            "risk_level": student.risk_level
        })
    
    return result

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student, User).join(User, Student.user_id == User.id).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_obj, user_obj = student
    
    return {
        "id": str(student_obj.id),
        "name": user_obj.name,
        "email": user_obj.email,
        "student_id": student_obj.student_id,
        "gpa": float(student_obj.gpa),
        "risk_score": student_obj.risk_score,
        "risk_level": student_obj.risk_level
    }