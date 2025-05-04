import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

def send_email_with_attachment(subject, body, recipient, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF file
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_path.split('/')[-1]}"
        )
        msg.attach(part)

    # Send email
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email_alert(subject, message, recipient):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

def send_email_alert(subject, message, recipient):
    ...


def send_email_with_attachment(subject, body, recipient, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject

    # HTML Body for better formatting
    html_body = f"""
    <html>
    <body>
        <p>{body}</p>
        <h3>Absentee Report for {datetime.today().strftime('%B %Y')}</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Absentee Count</th>
                </tr>
            </thead>
            <tbody>
    """

    for index, row in absentee_summary.iterrows():
        student_name = row['student_id']
        absentee_count = row['absentee_count']
        html_body += f"""
            <tr>
                <td>{student_name}</td>
                <td>{absentee_count}</td>
            </tr>
        """

    html_body += """
            </tbody>
        </table>
        <p>Kind regards,<br>Your Tuition Center Team</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    # Attach PDF file
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_path.split('/')[-1]}"
        )
        msg.attach(part)

    # Send email
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
