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
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import os
import base64
from app.config import SENDGRID_API_KEY, FROM_EMAIL

def send_email(recipients, subject, html_content):
    """
    Send email using SendGrid
    
    Args:
        recipients: List of email addresses to send to
        subject: Email subject
        html_content: HTML content of email
        
    Returns:
        Response from SendGrid API
    """
    try:
        # Create message
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipients,
            subject=subject,
            html_content=html_content
        )
        
        # Send message
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        return {
            "status": "success",
            "status_code": response.status_code
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }

def send_email_with_attachment(recipients, subject, html_content, attachment_path):
    """
    Send email with attachment using SendGrid
    
    Args:
        recipients: List of email addresses to send to
        subject: Email subject
        html_content: HTML content of email
        attachment_path: Path to attachment file
        
    Returns:
        Response from SendGrid API
    """
    try:
        # Create message
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipients,
            subject=subject,
            html_content=html_content
        )
        
        # Add attachment
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_base64 = base64.b64encode(file_data).decode()
            
        filename = os.path.basename(attachment_path)
        attachment = Attachment()
        attachment.file_content = FileContent(file_base64)
        attachment.file_name = FileName(filename)
        
        # Determine file type
        if filename.endswith('.pdf'):
            attachment.file_type = FileType('application/pdf')
        elif filename.endswith('.xlsx'):
            attachment.file_type = FileType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif filename.endswith('.csv'):
            attachment.file_type = FileType('text/csv')
        else:
            attachment.file_type = FileType('application/octet-stream')
            
        attachment.disposition = Disposition('attachment')
        message.attachment = attachment
        
        # Send message
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        return {
            "status": "success",
            "status_code": response.status_code
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }
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
