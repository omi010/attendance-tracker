from firebase_admin import firestore
import pandas as pd

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
