from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from app.database import Base
import uuid
from datetime import datetime

class Student(Base):
    __tablename__ = "students"

    # Use String for SQLite
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'))
    student_id = Column(String, unique=True, nullable=False)
    gpa = Column(Float, default=0.00)
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, default='low')
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)