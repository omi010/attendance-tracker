import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

from .data_exporter import export_attendance_data

def train_model():
    df["is_weekend"] = df["date"].dt.weekday >= 5
    # If you have a holiday list:
    holidays = ["2025-05-01", "2025-05-15"]
    df["is_holiday"] = df["date"].astype(str).isin(holidays)

    df = export_attendance_data()

    # Feature engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month

    # Create X and y
    X = df[['student_id', 'day', 'day_of_week', 'month']]
    y = df['present']

    # Encode student_id
    X = pd.get_dummies(X, columns=['student_id'])

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump((model, X.columns), "model/attendance_predictor.pkl")
    print("✅ Model trained and saved.")

