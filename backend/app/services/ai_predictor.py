import pandas as pd
import joblib
from datetime import datetime

# Dummy AI model for now
def predict_absentees_for_date(date: str):
    # In real case, use ML model + historical data
    # For demo: hardcoded sample
    likely_absent = ["abc123", "ghi789"]
    return likely_absent


def predict_absentees_for_date(date: str):
    model, columns = joblib.load("model/attendance_predictor.pkl")

    # Simulate all students on that day
    student_ids = ["abc123", "def456", "ghi789"]  # Ideally load from Firestore

    parsed = datetime.strptime(date, "%Y-%m-%d")
    features = []

    for sid in student_ids:
        row = {
            "day": parsed.day,
            "day_of_week": parsed.weekday(),
            "month": parsed.month,
            f"student_id_{sid}": 1
        }
        features.append(row)

    X = pd.DataFrame(features).fillna(0)
    X = X.reindex(columns=columns, fill_value=0)

    preds = model.predict(X)
    absentees = [student_ids[i] for i, p in enumerate(preds) if not p]
    return absentees
