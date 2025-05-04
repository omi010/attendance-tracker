from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from firebase_admin import firestore
from datetime import datetime
from app.services.ai_predictor import predict_absentees_for_date
from app.routes import report, attendance
from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from typing import List

app.include_router(report.router)
app.include_router(attendance.router)
@router.get("/download-absentees/{date}")
def download_absentees(date: str):
    """
    Downloads a report of absent students for the given date.
    """
    attendance_ref = db.collection("attendance").document(date).collection("students")
    docs = attendance_ref.stream()

    absent_students = []
    for doc in docs:
        data = doc.to_dict()
        if not data.get("present", True):  # default to True if not set
            student_ref = db.collection("students").document(doc.id)
            student = student_ref.get().to_dict()
            absent_students.append({
                "student_id": doc.id,
                "name": student.get("name", "Unknown"),
                "email": student.get("email", ""),
                "class": student.get("class", ""),
                "present": False,
                "date": date
            })

    # Save to Excel
    file_path = generate_excel_report(absent_students, f"absentees_{date}.xlsx")
    return FileResponse(file_path, filename=f"absentees_{date}.xlsx")

router = APIRouter()
db = firestore.client()

# Pydantic schema for incoming attendance data
class AttendanceEntry(BaseModel):
    student_id: str
    present: bool

# 🔸 Route to mark attendance for a given date
@router.post("/mark-attendance/{date}")
async def mark_attendance(date: str, entries: List[AttendanceEntry]):
    """
    Store attendance for a given date in Firestore:
    attendance/{date}/students/{student_id}
    """
    attendance_ref = db.collection("attendance").document(date).collection("students")

    for entry in entries:
        attendance_ref.document(entry.student_id).set({
            "present": entry.present,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

    return {"message": f"Attendance marked for {date}"}


# 🔹 Route to fetch daily attendance sheet
@router.get("/daily-sheet/{date}")
async def get_daily_sheet(date: str):
    """
    Return a list of students with their attendance for a given date.
    """
    attendance_ref = db.collection("attendance").document(date).collection("students")
    students_docs = attendance_ref.stream()

    sheet = []
    for doc in students_docs:
        data = doc.to_dict()
        sheet.append({
            "student_id": doc.id,
            "present": data.get("present", False),
            "timestamp": data.get("timestamp")
        })

    return sheet

router = APIRouter()
@router.get("/predict-absentees/{date}")
def predict_absentees(date: str):
    predicted = predict_absentees_for_date(date)
    return [{"student_id": sid} for sid in predicted]


router = APIRouter()


@router.get("/attendance/{date}", response_model=List[dict])
async def get_attendance_for_date(date: str):
    db = firestore.client()
    attendance_ref = db.collection("attendance").document(date).collection("students")

    students = attendance_ref.stream()

    attendance_data = []
    for student in students:
        student_data = student.to_dict()
        student_data["student_id"] = student.id
        attendance_data.append(student_data)

    if not attendance_data:
        raise HTTPException(status_code=404, detail="No attendance data found for this date")

    return attendance_data


from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Protected Admin Route
@router.get("/admin")
def read_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['sub'] != 'admin':
            raise HTTPException(status_code=403, detail="Forbidden")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")

    return {"message": "Welcome Admin"}


from fastapi import Depends, HTTPException
from app.auth import verify_token


@router.get("/admin")
def read_admin(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    return {"message": "Welcome Admin"}
from fastapi import Depends, HTTPException
from app.auth import verify_token

def role_required(role: str):
    def role_checker(token: str = Depends(oauth2_scheme)):
        payload = verify_token(token)
        if payload.get("role") != role:
            raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
        return payload
    return role_checker

# Admin Route
@router.get("/admin")
def read_admin(token: str = Depends(role_required("admin"))):
    return {"message": "Welcome Admin"}

# Teacher Route
@router.get("/teacher")
def read_teacher(token: str = Depends(role_required("teacher"))):
    return {"message": "Welcome Teacher"}

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import APIRouter, Depends

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/mark-attendance")
@limiter.limit("10/minute")  # Limit to 10 requests per minute
async def mark_attendance(request: Request):
    # Attendance marking logic here
    return {"message": "Attendance marked successfully"}

@router.get("/generate-report")
@limiter.limit("5/hour")  # Limit to 5 reports per hour
async def generate_report(request: Request):
    # Report generation logic here
    return {"message": "Report generated successfully"}
