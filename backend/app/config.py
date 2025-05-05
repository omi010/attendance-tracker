import os
from google.cloud import firestore
import os
from google.cloud import firestore

# Database
db = firestore.Client()

# Authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your-twilio-sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your-twilio-token")
TWILIO_PHONE = os.getenv("TWILIO_PHONE", "+1234567890")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+9876543210")
import os
from google.cloud import firestore

# Database
db = firestore.Client()

# Application Settings
APP_NAME = os.getenv("APP_NAME", "Student Attendance Tracker")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]
ABSENTEE_THRESHOLD = int(os.getenv("ABSENTEE_THRESHOLD", "5"))
REPORT_FOLDER = os.getenv("REPORT_FOLDER", "reports")
MODEL_FOLDER = os.getenv("MODEL_FOLDER", "model")

# Authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your-twilio-sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your-twilio-token") 
TWILIO_PHONE = os.getenv("TWILIO_PHONE", "+1234567890")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+9876543210")

# SendGrid Email Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "your-sendgrid-api-key")
FROM_EMAIL = os.getenv("FROM_EMAIL", "attendance@example.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

# AI Model Settings
RETRAIN_MODEL_WEEKLY = os.getenv("RETRAIN_MODEL_WEEKLY", "True").lower() in ["true", "1", "t"]
MODEL_ACCURACY_THRESHOLD = float(os.getenv("MODEL_ACCURACY_THRESHOLD", "0.75"))

# Create folders if they don't exist
for folder in [REPORT_FOLDER, MODEL_FOLDER]:
    os.makedirs(folder, exist_ok=True)
# SendGrid Email Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "your-sendgrid-api-key")
FROM_EMAIL = os.getenv("FROM_EMAIL", "attendance@example.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

# Application Settings
ABSENTEE_THRESHOLD = 5
APP_NAME = "Student Attendance Tracker"
REPORT_FOLDER = "reports"
MODEL_FOLDER = "model"
# Initialize Firestore DB
db = firestore.Client()

# Twilio
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
ADMIN_PHONE = os.getenv("ADMIN_PHONE")

# JWT Secret
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
