from fastapi import FastAPI
from app.routes import student, attendance
from app.config import db
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pytesseract
from PIL import Image
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.routes.report import send_all_reports
from app.services.scheduler import start_scheduler
from fastapi import FastAPI
from twilio.rest import Client
from app.config import TWILIO_PHONE, ADMIN_PHONE
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from app.routes.auth import router as auth_router
from fastapi import Depends, HTTPException
from app.services.auth import verify_password


@app.post("/login")
async def login(email: str, password: str):
    user = get_user_from_firestore(email)  # Fetch user from Firestore
    if not user or not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token if credentials are correct
    access_token = create_access_token(user)
    return {"access_token": access_token}

# Twilio client setup
twilio_client = Client()

def send_sms_alert(student):
    # SMS body
    message = f"ALERT: High absentee count for {student['student_id']}! Absentee Count: {student['absentee_count']}."

    # Send SMS to admin
    twilio_client.messages.create(
        to=ADMIN_PHONE,
        from_=TWILIO_PHONE,
        body=message
    )

def check_for_high_absentee_counts():
    absentee_threshold = 5
    high_absentee_students = retrieve_high_absentee_students(absentee_threshold)

    for student in high_absentee_students:
        send_sms_alert(student)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    start_scheduler()  # Start the scheduler on app startup


app = FastAPI()

# Function that sends daily absentee alerts
def send_daily_absentee_alerts():
    # Logic to check attendance and send emails
    print("Sending absentee alerts...")

# Create an instance of the scheduler
scheduler = BlockingScheduler()

# Add a job that runs the function every 24 hours, starting from a specific time
scheduler.add_job(send_daily_absentee_alerts, 'interval', hours=24, start_date='2025-05-04 18:00:00')

# Start the scheduler
scheduler.start()

@app.on_event("startup")
async def on_startup():
    start_scheduler()  # Start the background scheduler when the app starts

@app.get("/")
def read_root():
    return {"message": "Attendance Tracker API running"}
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_all_reports("2025-05"), 'cron', day=1, hour=9)
    scheduler.start()

def generate_excel_report(data):
    df = pd.DataFrame(data)
    df.to_excel("attendance.xlsx")

app = FastAPI()

app.include_router(student.router)
app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"message": "Attendance Tracker API running"}

def extract_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

email_body = {
    "en": f"Your child was present for {days} days in {month}.",
    "hi": f"आपका बच्चा {month} में {days} दिनों के लिए उपस्थित था।"
}[language]

@router.get("/download-report/{month}")
def download_report(month: str, class_name: str = None):
    report_data = get_monthly_summary(month, class_name)
    ...


def start_alert_scheduler():
    scheduler = BackgroundScheduler()

    # Check for high absentee counts daily at 10 AM
    scheduler.add_job(check_for_high_absentee_counts, 'cron', hour=10, minute=0)

    scheduler.start()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.limiter = limiter

# Applying rate limiting to the login route
@app.post("/token")
@limiter.limit("5/minute")  # Limit to 5 requests per minute
async def login(request: Request):
    # Your existing login logic here
    return {"message": "Login successful"}

@app.post("/attendance")
@limiter.limit("10/minute", error_message="Too many requests. Please try again later.")
async def mark_attendance(request: Request):
    pass