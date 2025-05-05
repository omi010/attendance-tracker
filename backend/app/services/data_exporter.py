from firebase_admin import firestore
import pandas as pd
import pandas as pd
from app.config import db
from datetime import datetime

def export_attendance_data(start_date=None, end_date=None, class_id=None, format="dataframe"):
    """
    Export attendance data from Firestore
    
    Args:
        start_date: Optional start date filter (string "YYYY-MM-DD" or datetime)
        end_date: Optional end date filter (string "YYYY-MM-DD" or datetime)
        class_id: Optional class ID filter
        format: Output format ("dataframe", "csv", "excel")
        
    Returns:
        Pandas DataFrame or file path depending on format
    """
    # Get attendance records
    query = db.collection("attendance")
    
    # Apply filters
    if start_date:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where("date", ">=", start_date)
        
    if end_date:
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.where("date", "<=", end_date)
        
    if class_id:
        query = query.where("class_id", "==", class_id)
    
    # Execute query and convert to DataFrame
    records = []
    for doc in query.stream():
        attendance_data = doc.to_dict()
        attendance_data["id"] = doc.id
        records.append(attendance_data)
    
    df = pd.DataFrame(records)
    
    # Create 'present' column (1 for present, 0 for absent)
    if 'status' in df.columns:
        df['present'] = df['status'].apply(lambda x: 1 if x == 'present' else 0)
    
    # Handle format
    if format == "csv":
        file_path = "reports/attendance.csv"
        df.to_csv(file_path, index=False)
        return file_path
    elif format == "excel":
        file_path = "reports/attendance.xlsx"
        df.to_excel(file_path, index=False)
        return file_path
    else:  # Default: return DataFrame
        return df
def export_attendance_data():
    db = firestore.client()
    attendance_ref = db.collection("attendance")

    rows = []
    for day_doc in attendance_ref.stream():
        date = day_doc.id
        student_docs = attendance_ref.document(date).collection("students").stream()
        for s in student_docs:
            data = s.to_dict()
            rows.append({
                "date": date,
                "student_id": s.id,
                "present": data.get("present", False)
            })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df
