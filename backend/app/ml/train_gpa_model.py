import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import json

def train_gpa_model():
    print("=" * 50)
    print("TRAINING GPA PREDICTION MODEL")
    print("=" * 50)
    
    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('student_data.csv')
    print(f"✅ Loaded {len(df)} records")
    
    # Select features
    features = [
        'age',
        'previous_gpa',
        'current_gpa',
        'attendance_rate',
        'assignment_completion',
        'study_hours_per_week',
        'forum_posts',
        'days_since_last_login'
    ]
    
    X = df[features]
    y = df['predicted_gpa']  # Target: next semester GPA
    
    print(f"\n2. Predicting: Next semester GPA")
    print(f"   Current GPA range: {df['current_gpa'].min():.2f} - {df['current_gpa'].max():.2f}")
    print(f"   Predicted GPA range: {y.min():.2f} - {y.max():.2f}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\n3. Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    print("✅ Model trained!")
    
    # Evaluate
    print("\n4. Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📊 RESULTS:")
    print(f"   Mean Absolute Error: {mae:.3f}")
    print(f"   Root Mean Squared Error: {rmse:.3f}")
    print(f"   R² Score: {r2:.3f}")
    
    # Feature importance
    print(f"\n📈 Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance)
    
    # Save model
    print("\n5. Saving model...")
    joblib.dump(model, 'gpa_model.pkl')
    joblib.dump(scaler, 'gpa_scaler.pkl')
    
    with open('gpa_features.json', 'w') as f:
        json.dump(features, f)
    
    print("✅ Model saved as 'gpa_model.pkl'")
    print("✅ Scaler saved as 'gpa_scaler.pkl'")
    
    # Test prediction
    print("\n6. Testing with sample student...")
    sample = X_test.iloc[0:1]
    sample_scaled = scaler.transform(sample)
    prediction = model.predict(sample_scaled)[0]
    actual = y_test.iloc[0]
    
    print(f"   Current GPA: {sample['current_gpa'].values[0]:.2f}")
    print(f"   Predicted next GPA: {prediction:.2f}")
    print(f"   Actual next GPA: {actual:.2f}")
    print(f"   Error: {abs(prediction - actual):.3f}")
    
    print("\n" + "=" * 50)
    print("✅ GPA MODEL TRAINING COMPLETE!")
    print("=" * 50)
    
    return model, scaler

if __name__ == "__main__":
    train_gpa_model()