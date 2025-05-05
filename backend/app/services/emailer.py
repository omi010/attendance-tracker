import smtplib
from email.message import EmailMessage
import logging
from datetime import datetime, timedelta
from app.config import db, ADMIN_EMAIL, FROM_EMAIL
from app.services.email_service import send_email

# Initialize logger
logger = logging.getLogger(__name__)

def get_yesterday_absentees():
    """
    Get a list of students who were absent yesterday
    
    Returns:
        List of student records with their details
    """
    try:
        # Calculate yesterday's date
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        # Query for absent students
        absent_records = db.collection("attendance") \
            .where("date", "==", yesterday_str) \
            .where("status", "==", "absent") \
            .stream()
            
        # Get student details for each absent student
        absentees = []
        for record in absent_records:
            data = record.to_dict()
            
            # Get student details
            student_id = data.get("student_id")
            if student_id:
                student_doc = db.collection("students").document(student_id).get()
                if student_doc.exists:
                    student_data = student_doc.to_dict()
                    absentees.append({
                        "id": student_id,
                        "name": student_data.get("name", "Unknown"),
                        "email": student_data.get("email", ""),
                        "class_id": student_data.get("class_id", ""),
                        "parent_phone": student_data.get("parent_phone", "")
                    })
                
        return absentees
    except Exception as e:
        logger.error(f"Error getting yesterday's absentees: {str(e)}")
        return []

def send_daily_absentee_alerts():
    """
    Send a daily email report of students absent the previous day
    """
    try:
        # Get yesterday's date for the subject
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        # Get absentee list
        absentees = get_yesterday_absentees()
        
        if not absentees:
            logger.info(f"No absentees found for {yesterday_str}")
            return
            
        # Build email content
        subject = f"Daily Absence Report for {yesterday_str}"
        
        # Create HTML table of absentees
        html_content = f"""
        <h2>Absence Report for {yesterday_str}</h2>
        <p>The following students were absent yesterday:</p>
        <table border="1">
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Class</th>
            </tr>
        """
        
        for student in absentees:
            html_content += f"""
            <tr>
                <td>{student['id']}</td>
                <td>{student['name']}</td>
                <td>{student['class_id']}</td>
            </tr>
            """
            
        html_content += """
        </table>
        <p>Please take appropriate action.</p>
        """
        
        # Send email to admin
        result = send_email(
            recipients=[ADMIN_EMAIL],
            subject=subject,
            html_content=html_content
        )
        
        if result.get("status") == "success":
            logger.info(f"Daily absence report sent with {len(absentees)} students")
        else:
            logger.error(f"Failed to send daily absence report: {result.get('message')}")
            
    except Exception as e:
        logger.error(f"Error sending daily absentee alerts: {str(e)}")
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
