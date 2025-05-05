import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime
from app.config import MODEL_FOLDER

from .data_exporter import export_attendance_data

def train_model():
    # Get data
    df = export_attendance_data()
    
    # Check if dataframe is empty
    if df.empty or len(df) < 10:
        print("⚠️ Not enough data to train model")
        return False
    
    # Convert date column to datetime if it's not already
    if 'date' in df.columns and not pd.api.types.is_datetime64_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])
    
    # Feature engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df["is_weekend"] = df["date"].dt.weekday >= 5
    
    # If you have a holiday list:
    holidays = ["2025-05-01", "2025-05-15"]
    df["is_holiday"] = df["date"].astype(str).isin(holidays)

    # Create X and y
    X = df[['student_id', 'day', 'day_of_week', 'month', 'is_weekend', 'is_holiday']]
    
    if 'present' not in df.columns:
        print("⚠️ Dataset doesn't contain 'present' column")
        return False
        
    y = df['present']

    # Encode student_id
    X = pd.get_dummies(X, columns=['student_id'])

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Test model accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    # Create model directory if it doesn't exist
    os.makedirs(MODEL_FOLDER, exist_ok=True)
    
    # Save model
    model_path = f"{MODEL_FOLDER}/attendance_predictor.pkl"
    joblib.dump((model, X.columns), model_path)
    print(f"✅ Model trained and saved to {model_path}")
    
    return True

