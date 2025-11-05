import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_student_data(num_students=500):
    """Generate synthetic student data for training ML models"""
    
    np.random.seed(42)
    random.seed(42)
    
    students = []
    
    for i in range(num_students):
        # Base characteristics
        student_id = f"STU{i:04d}"
        age = random.randint(18, 25)
        
        # Academic history
        previous_gpa = round(np.random.normal(3.0, 0.8), 2)
        previous_gpa = max(0, min(4.0, previous_gpa))  # Clamp between 0-4
        
        # Behavioral factors
        attendance_rate = round(np.random.normal(85, 15), 2)
        attendance_rate = max(0, min(100, attendance_rate))
        
        assignment_completion = round(np.random.normal(80, 20), 2)
        assignment_completion = max(0, min(100, assignment_completion))
        
        study_hours_per_week = max(0, int(np.random.normal(15, 8)))
        
        # Engagement metrics
        forum_posts = max(0, int(np.random.normal(10, 5)))
        days_since_last_login = max(0, int(np.random.exponential(2)))
        
        # Financial/personal factors
        financial_aid = random.choice([0, 1])
        part_time_job = random.choice([0, 1])
        commute_time = max(0, int(np.random.normal(30, 20)))
        
        # Calculate risk factors
        risk_factors = []
        if attendance_rate < 70:
            risk_factors.append(0.3)
        if assignment_completion < 60:
            risk_factors.append(0.25)
        if days_since_last_login > 7:
            risk_factors.append(0.2)
        if previous_gpa < 2.5:
            risk_factors.append(0.3)
        if study_hours_per_week < 10:
            risk_factors.append(0.15)
        
        # Calculate current GPA with some correlation to factors
        gpa_base = previous_gpa
        gpa_adjustment = (attendance_rate / 100) * 0.5 + \
                        (assignment_completion / 100) * 0.5 + \
                        (study_hours_per_week / 30) * 0.3 - \
                        (days_since_last_login / 14) * 0.2
        
        current_gpa = round(max(0, min(4.0, gpa_base + gpa_adjustment + np.random.normal(0, 0.3))), 2)
        
        # Dropout probability (0-100)
        risk_score = sum(risk_factors) * 100 if risk_factors else random.randint(5, 30)
        risk_score = int(min(100, max(0, risk_score + np.random.normal(0, 10))))
        
        # Predict next semester GPA
        predicted_gpa = round(current_gpa + np.random.normal(0, 0.2), 2)
        predicted_gpa = max(0, min(4.0, predicted_gpa))
        
        # Create dropout label (1 = at risk, 0 = safe)
        dropout_risk = 1 if risk_score > 60 else 0
        
        student = {
            'student_id': student_id,
            'age': age,
            'previous_gpa': previous_gpa,
            'current_gpa': current_gpa,
            'predicted_gpa': predicted_gpa,
            'attendance_rate': attendance_rate,
            'assignment_completion': assignment_completion,
            'study_hours_per_week': study_hours_per_week,
            'forum_posts': forum_posts,
            'days_since_last_login': days_since_last_login,
            'financial_aid': financial_aid,
            'part_time_job': part_time_job,
            'commute_time': commute_time,
            'risk_score': risk_score,
            'dropout_risk': dropout_risk
        }
        
        students.append(student)
    
    df = pd.DataFrame(students)
    return df

# Generate and save data
if __name__ == "__main__":
    print("Generating synthetic student data...")
    df = generate_student_data(500)
    
    # Save to CSV
    df.to_csv('student_data.csv', index=False)
    print(f"✅ Generated {len(df)} student records")
    print(f"✅ Saved to student_data.csv")
    print(f"\nDataset Info:")
    print(df.head())
    print(f"\nDropout Risk Distribution:")
    print(df['dropout_risk'].value_counts())