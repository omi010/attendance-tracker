import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("path/to/your-serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

TWILIO_PHONE = "your_twilio_phone_number"
ADMIN_PHONE = "admin_phone_number"

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
