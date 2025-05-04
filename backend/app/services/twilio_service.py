from twilio.rest import Client
from dotenv import load_dotenv
import os
client = Client(account_sid, auth_token)

def send_alert(contact, message):
    client.messages.create(body=message, from_='whatsapp:+14155238886', to=f'whatsapp:{contact}')
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_sms_alert(message: str, to: str):
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to
    )
    return message.sid
