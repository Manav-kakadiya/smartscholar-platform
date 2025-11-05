import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import json

def train_dropout_model():
    print("=" * 50)
    print("TRAINING DROPOUT PREDICTION MODEL")
    print("=" * 50)
    
    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('student_data.csv')
    print(f"✅ Loaded {len(df)} records")
    
    # Select features for prediction
    features = [
        'age',
        'previous_gpa',
        'current_gpa',
        'attendance_rate',
        'assignment_completion',
        'study_hours_per_week',
        'forum_posts',
        'days_since_last_login',
        'financial_aid',
        'part_time_job',
        'commute_time'
    ]
    
    X = df[features]
    y = df['dropout_risk']  # 0 or 1
    
    print(f"\n2. Features selected: {len(features)}")
    print(f"   Class distribution:")
    print(f"   - Safe (0): {(y == 0).sum()} students")
    print(f"   - At Risk (1): {(y == 1).sum()} students")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n3. Data split:")
    print(f"   - Training: {len(X_train)} samples")
    print(f"   - Testing: {len(X_test)} samples")
    
    # Scale features
    print("\n4. Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\n5. Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    print("✅ Model trained!")
    
    # Evaluate
    print("\n6. Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📊 RESULTS:")
    print(f"   Accuracy: {accuracy:.2%}")
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'At Risk']))
    
    # Feature importance
    print(f"\n📈 Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance)
    
    # Save model
    print("\n7. Saving model...")
    joblib.dump(model, 'dropout_model.pkl')
    joblib.dump(scaler, 'dropout_scaler.pkl')
    
    # Save feature names
    with open('dropout_features.json', 'w') as f:
        json.dump(features, f)
    
    print("✅ Model saved as 'dropout_model.pkl'")
    print("✅ Scaler saved as 'dropout_scaler.pkl'")
    print("✅ Features saved as 'dropout_features.json'")
    
    # Test with sample prediction
    print("\n8. Testing with sample student...")
    sample_student = X_test.iloc[0:1]
    sample_scaled = scaler.transform(sample_student)
    prediction = model.predict(sample_scaled)[0]
    probability = model.predict_proba(sample_scaled)[0]
    
    print(f"   Student data: {sample_student.values[0]}")
    print(f"   Prediction: {'At Risk' if prediction == 1 else 'Safe'}")
    print(f"   Probability: {probability[1]:.2%} at risk")
    
    print("\n" + "=" * 50)
    print("✅ DROPOUT MODEL TRAINING COMPLETE!")
    print("=" * 50)
    
    return model, scaler

if __name__ == "__main__":
    train_dropout_model()