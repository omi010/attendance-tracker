from fastapi import APIRouter, Request
from app.config import db
from twilio.rest import Client
from app.config import TWILIO_PHONE, ADMIN_PHONE

router = APIRouter(prefix="/attendance")
twilio_client = Client()

@router.post("/")
async def mark_attendance(request: Request):
    data = await request.json()
    db.collection("attendance").add(data)
    return {"message": "Attendance marked"}

def retrieve_high_absentee_students(threshold: int):
    students = db.collection("students").stream()
    high_absentees = []

    for student in students:
        student_data = student.to_dict()
        absent_q = db.collection("attendance").where("student_id", "==", student_data["id"]).where("status", "==", "absent")
        if len(list(absent_q.stream())) >= threshold:
            high_absentees.append({
                "student_id": student_data["id"],
                "absentee_count": len(list(absent_q.stream()))
            })
    return high_absentees

def send_sms_alert(student):
    message = f"ALERT: {student['student_id']} has {student['absentee_count']} absences!"
    twilio_client.messages.create(
        to=ADMIN_PHONE,
        from_=TWILIO_PHONE,
        body=message
    )

def check_for_high_absentee_counts():
    for s in retrieve_high_absentee_students(5):
        send_sms_alert(s)
