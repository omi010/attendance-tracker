import smtplib
from email.message import EmailMessage

def send_email_with_attachment(to_email, subject, body, file_path):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "youremail@gmail.com"
    msg["To"] = to_email
    msg.set_content(body)

    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = file_path.split("/")[-1]

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("youremail@gmail.com", "YOUR_APP_PASSWORD")
        smtp.send_message(msg)
