from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.routes import student, attendance
from app.routes.auth import router as auth_router
from app.routes.report import send_all_reports, get_monthly_summary
from app.services.scheduler import start_all_schedulers
from app.services.auth import verify_password, create_access_token, get_user_from_firestore
from app.routes.attendance import retrieve_high_absentee_students
from app.config import (
    db, TWILIO_PHONE, ADMIN_PHONE, TWILIO_ACCOUNT_SID, 
    TWILIO_AUTH_TOKEN, APP_NAME, ABSENTEE_THRESHOLD
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from PIL import Image
import pytesseract
import pandas as pd
import base64
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI and rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title=APP_NAME,
    description="API for student attendance tracking system",
    version="1.0.0"
)
app.state.limiter = limiter

# Include routers
app.include_router(student.router)
app.include_router(attendance.router)
app.include_router(auth_router)

# --- Login Route ---
@app.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = get_user_from_firestore(form_data.username)
        if not user or not verify_password(form_data.password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )
        return {"access_token": create_access_token(user), "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

# --- OCR Text Extraction ---
def extract_text(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        logger.error(f"OCR error: {str(e)}")
        return None

# --- Generate Excel Report ---
def generate_excel_report(data):
    try:
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        file_path = "reports/attendance.xlsx"
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        return file_path
    except Exception as e:
        logger.error(f"Excel generation error: {str(e)}")
        return None

# --- Twilio SMS Alert ---
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    logger.error(f"Twilio client initialization error: {str(e)}")
    twilio_client = None

def send_sms_alert(student):
    if not twilio_client:
        logger.error("Twilio client not initialized")
        return False
        
    try:
        message = f"ALERT: High absentee count for {student['student_id']}! Absentee Count: {student['absentee_count']}."
        twilio_client.messages.create(
            to=ADMIN_PHONE,
            from_=TWILIO_PHONE,
            body=message
        )
        return True
    except Exception as e:
        logger.error(f"SMS alert error: {str(e)}")
        return False

def check_for_high_absentee_counts():
    try:
        high_absentee_students = retrieve_high_absentee_students(ABSENTEE_THRESHOLD)
        for student in high_absentee_students:
            send_sms_alert(student)
        logger.info(f"Checked absences for {len(high_absentee_students)} students")
    except Exception as e:
        logger.error(f"Error checking absentee counts: {str(e)}")

# --- Alert Scheduler ---
def start_alert_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_high_absentee_counts, 'cron', hour=10, minute=0)
    scheduler.start()
    logger.info("Alert scheduler started")

# --- Report Scheduler ---
def start_report_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_all_reports("2025-05"), 'cron', day=1, hour=9)
    scheduler.start()
    logger.info("Report scheduler started")

# --- Daily Email Alerts ---
def send_daily_absentee_alerts():
    logger.info("Sending daily absentee alerts")
    try:
        # Add implementation here
        pass
    except Exception as e:
        logger.error(f"Error sending daily alerts: {str(e)}")

# --- App Startup Event ---
@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {APP_NAME}")
    start_all_schedulers()

# --- App Shutdown Event ---
@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"Shutting down {APP_NAME}")

# --- Root Endpoint ---
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": f"{APP_NAME} running", "status": "active"}

# --- Health Check Endpoint ---
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# --- Report Download Endpoint ---
@app.get("/download-report/{month}", status_code=status.HTTP_200_OK)
def download_report(month: str, class_name: str = None):
    try:
        report_data = get_monthly_summary(month, class_name)
        
        if "error" in report_data:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": report_data["error"]}
            )
            
        return {"report": report_data}
    except Exception as e:
        logger.error(f"Report download error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the report"
        )
