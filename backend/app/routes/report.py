from fastapi import APIRouter
from firebase_admin import firestore
from datetime import datetime
from collections import defaultdict
from fastapi.responses import FileResponse
from app.utils.excel_export import generate_excel_report
from app.utils.pdf_export import generate_pdf_report
from app.services.report_builder import get_monthly_summary
from app.services.emailer import send_email_with_attachment  # or send_report_sendgrid
import os
from app.services.twilio_service import send_sms_alert
from app.services.email_service import send_email_alert
from fastapi import APIRouter, HTTPException
from app.services.report_generator import generate_daily_report, generate_class_report, generate_monthly_absentee_report
from pydantic import BaseModel
from typing import List, Optional

@router.post("/email-absentees/{date}")
def email_absentee_parents(date: str):
    attendance_ref = db.collection("attendance").document(date).collection("students")
    docs = attendance_ref.stream()

    absentees = []
    for doc in docs:
        data = doc.to_dict()
        if not data.get("present", True):
            student_id = doc.id
            student = db.collection("students").document(student_id).get().to_dict()
            if student and "email" in student:
                name = student.get("name", "Student")
                email = student["email"]
                message = f"Dear Parent,\n\nThis is to inform you that {name} was absent on {date}.\n\n- Tuition Center"
                send_email_alert(f"Absence Notice for {name}", message, email)
                absentees.append({"name": name, "email": email})

    return {"status": "sent", "count": len(absentees), "absentees": absentees}

if len(absentees) > threshold:
    subject = "High Absentee Alert"
    body = f"{len(absentees)} students are absent on {date}. Please review the attendance sheet."
    admin_email = "admin@example.com"
    send_email_alert(subject, body, admin_email)

@router.get("/check-absentees-alert/{date}")
def check_absentee_alert(date: str, threshold: int = 10):
    attendance_ref = db.collection("attendance").document(date).collection("students")
    docs = attendance_ref.stream()

    absentees = [doc.id for doc in docs if not doc.to_dict().get("present", True)]

    if len(absentees) > threshold:
        alert_msg = f"⚠️ High Absentee Alert: {len(absentees)} students absent on {date}"
        # Replace with real admin/teacher phone number
        admin_phone = "+911234567890"
        send_sms_alert(alert_msg, admin_phone)
        return {"status": "sent", "message": alert_msg}

    return {"status": "ok", "message": f"{len(absentees)} absentees – below threshold"}


router = APIRouter()
@router.get("/download-absentees-preview/{date}")
def absentee_preview(date: str):
    attendance_ref = db.collection("attendance").document(date).collection("students")
    docs = attendance_ref.stream()

    absentees = []
    for doc in docs:
        data = doc.to_dict()
        if not data.get("present", True):
            student_ref = db.collection("students").document(doc.id)
            student = student_ref.get().to_dict()
            absentees.append({
                "student_id": doc.id,
                "name": student.get("name", "Unknown"),
                "email": student.get("email", ""),
                "class": student.get("class", ""),
            })

    return absentees

@router.get("/download-report/{month}")
def download_report(month: str):
    report_data = get_monthly_summary(month)
    file_path = generate_excel_report(report_data, f"{month}_report.xlsx")

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, filename=f"{month}_report.xlsx",
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@router.post("/send-monthly-reports/{month}")
def send_all_reports(month: str):
    report_data = get_monthly_summary(month)

    for student in report_data:
        html = f"""
        <h1>Attendance Report for {student['name']}</h1>
        <p>Present Days in {month}: {student['present_days']}</p>
        """
        file_path = generate_pdf_report(html, f"{student['student_id']}_report.pdf")
        send_email_with_attachment(student["email"], "Your Monthly Attendance Report", "Please see attached.", file_path)

    return {"message": "All reports emailed successfully."}

router = APIRouter()
db = firestore.client()

@router.get("/monthly-summary/{month}")
def get_monthly_summary(month: str):
    """
    Month format: YYYY-MM (e.g., 2025-05)
    """
    year, month_num = month.split("-")
    prefix = f"{year}-{month_num.zfill(2)}"
    attendance_ref = db.collection("attendance")
    docs = attendance_ref.stream()

    student_counts = defaultdict(int)

    for doc in docs:
        doc_id = doc.id
        if not doc_id.startswith(prefix):
            continue

        student_docs = attendance_ref.document(doc_id).collection("students").stream()
        for s in student_docs:
            data = s.to_dict()
            if data.get("present"):
                student_counts[s.id] += 1

    result = [{"student_id": sid, "present_days": count} for sid, count in student_counts.items()]
    return result

# backend/app/routes/report.py
@router.get("/monthly-report/excel/{month}")
def get_excel_report(month: str):
    summary = get_monthly_summary(month)
    file_path = generate_excel_report(summary)
    return FileResponse(path=file_path, filename="attendance_report.xlsx", media_type="application/vnd.ms-excel")

@router.get("/monthly-report/pdf/{month}")
def get_pdf_report(month: str):
    summary = get_monthly_summary(month)
    html = "<h1>Monthly Report</h1><table><tr><th>Student</th><th>Days Present</th></tr>"
    for entry in summary:
        html += f"<tr><td>{entry['student_id']}</td><td>{entry['present_days']}</td></tr>"
    html += "</table>"
    file_path = generate_pdf_report(html)
    return FileResponse(path=file_path, filename="attendance_report.pdf", media_type="application/pdf")

router = APIRouter()

class ReportRequest(BaseModel):
    report_type: str
    date: str = None  # Optional for daily
    class_name: str = None  # Optional for class report

@router.post("/generate-report")
async def generate_report(request: ReportRequest):
    if request.report_type == "daily" and request.date:
        return generate_daily_report(request.date)
    elif request.report_type == "class" and request.class_name:
        return generate_class_report(request.class_name, request.date)
    elif request.report_type == "monthly":
        return generate_monthly_absentee_report(request.date)
    else:
        raise HTTPException(status_code=400, detail="Invalid report request")


router = APIRouter()


@router.get("/attendance/{date}", response_model=List[dict])
async def get_attendance_for_date(
        date: str,
        class_name: Optional[str] = None,
        student_name: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
):
    db = firestore.client()
    attendance_ref = db.collection("attendance").document(date).collection("students")

    # Apply filters if provided
    if class_name:
        attendance_ref = attendance_ref.where('class', '==', class_name)

    if student_name:
        attendance_ref = attendance_ref.where('student_name', '==', student_name)

    if from_date and to_date:
        attendance_ref = attendance_ref.where('timestamp', '>=', from_date).where('timestamp', '<=', to_date)

    students = attendance_ref.stream()

    attendance_data = []
    for student in students:
        student_data = student.to_dict()
        student_data["student_id"] = student.id
        attendance_data.append(student_data)

    if not attendance_data:
        raise HTTPException(status_code=404, detail="No attendance data found")

    return attendance_data