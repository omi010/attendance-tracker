from firebase_admin import firestore
from collections import defaultdict

def get_monthly_summary(month: str, class_name: str = None):
    ...
    for student_id, present_days in summary.items():
        student_doc = students_ref.document(student_id).get()
        student_data = student_doc.to_dict()

        if class_name and student_data.get("class") != class_name:
            continue

        final_report.append({
            "student_id": student_id,
            "name": student_data.get("name", ""),
            "email": student_data.get("email", ""),
            "class": student_data.get("class", ""),
            "present_days": present_days
        })

def get_monthly_summary(month: str):
    db = firestore.client()
    attendance_ref = db.collection("attendance")
    students_ref = db.collection("students")

    summary = defaultdict(int)

    for doc in attendance_ref.stream():
        if not doc.id.startswith(month):  # Only get entries from requested month
            continue
        student_docs = attendance_ref.document(doc.id).collection("students").stream()
        for s in student_docs:
            if s.to_dict().get("present"):
                summary[s.id] += 1

    final_report = []
    for student_id, present_days in summary.items():
        student_doc = students_ref.document(student_id).get()
        student_data = student_doc.to_dict()
        final_report.append({
            "student_id": student_id,
            "name": student_data.get("name", ""),
            "email": student_data.get("email", ""),
            "present_days": present_days
        })

    return final_report

