from fastapi import APIRouter
from app.config import db
import pandas as pd

router = APIRouter(prefix="/reports")

def get_monthly_summary(month: str, class_name: str = None):
    records = db.collection("attendance").where("month", "==", month).stream()
    data = [r.to_dict() for r in records if not class_name or r.to_dict().get("class") == class_name]
    return data

def send_all_reports(month: str):
    data = get_monthly_summary(month)
    df = pd.DataFrame(data)
    filename = f"{month}_summary.xlsx"
    df.to_excel(filename, index=False)
    print(f"[Report] Sent monthly report: {filename}")
from fastapi import APIRouter, HTTPException, Depends
from app.config import db, FROM_EMAIL, ADMIN_EMAIL
from app.services.data_exporter import export_attendance_data
from app.utils.pdf_export import generate_pdf_report
from app.services.email_service import send_email_with_attachment
import pandas as pd
from datetime import datetime
import os

router = APIRouter(prefix="/reports")

def get_monthly_summary(month: str, class_name: str = None):
    """
    Generate monthly attendance summary data
    
    Args:
        month: Month in format "YYYY-MM"
        class_name: Optional class name to filter by
        
    Returns:
        Dictionary with attendance summary data
    """
    try:
        year, month_num = month.split("-")
        start_date = f"{year}-{month_num}-01"
        
        # Calculate end date (last day of month)
        if month_num == "12":
            end_date = f"{int(year)+1}-01-01"
        else:
            next_month = int(month_num) + 1
            end_date = f"{year}-{next_month:02d}-01"
            
        # Get attendance data
        df = export_attendance_data(start_date=start_date, end_date=end_date, class_id=class_name)
        
        if df.empty:
            return {"error": "No attendance data found for this period"}
            
        # Calculate summaries
        student_summary = df.groupby('student_id')['present'].agg(['sum', 'count']).reset_index()
        student_summary['percentage'] = (student_summary['sum'] / student_summary['count'] * 100).round(1)
        student_summary.columns = ['student_id', 'days_present', 'total_days', 'attendance_percentage']
        
        # Get overall stats
        total_students = len(student_summary)
        avg_attendance = student_summary['attendance_percentage'].mean()
        perfect_attendance = len(student_summary[student_summary['attendance_percentage'] == 100])
        
        return {
            "month": month,
            "class_name": class_name,
            "total_students": total_students,
            "average_attendance": avg_attendance,
            "perfect_attendance_count": perfect_attendance,
            "student_details": student_summary.to_dict('records')
        }
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/monthly/{month}")
def get_report(month: str, class_name: str = None):
    """API endpoint to get monthly attendance report"""
    report_data = get_monthly_summary(month, class_name)
    return report_data

def send_report_email(month: str, recipients: list, class_name: str = None):
    """Send attendance report via email"""
    try:
        # Get report data
        report_data = get_monthly_summary(month, class_name)
        
        # Generate HTML for the report
        html_content = f"""
        <h1>Attendance Report: {month}</h1>
        <p>Class: {class_name if class_name else 'All Classes'}</p>
        <p>Average Attendance: {report_data['average_attendance']:.1f}%</p>
        <p>Students with Perfect Attendance: {report_data['perfect_attendance_count']}</p>
        
        <h2>Student Details</h2>
        <table border="1">
            <tr>
                <th>Student ID</th>
                <th>Days Present</th>
                <th>Total Days</th>
                <th>Attendance %</th>
            </tr>
        """
        
        for student in report_data['student_details']:
            html_content += f"""
            <tr>
                <td>{student['student_id']}</td>
                <td>{student['days_present']}</td>
                <td>{student['total_days']}</td>
                <td>{student['attendance_percentage']}%</td>
            </tr>
            """
            
        html_content += "</table>"
        
        # Generate PDF
        pdf_path = generate_pdf_report(html_content, f"attendance_report_{month}.pdf")
        
        # Send email
        subject = f"Attendance Report - {month}"
        body = f"Please find attached the attendance report for {month}."
        
        # Send email with attachment
        send_email_with_attachment(
            recipients=recipients,
            subject=subject,
            html_content=body,
            attachment_path=pdf_path
        )
        
        return {"status": "success", "message": f"Report sent to {', '.join(recipients)}"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_all_reports(month: str):
    """Send reports to all administrators"""
    return send_report_email(
        month=month,
        recipients=[ADMIN_EMAIL],
        class_name=None  # Send all classes
    )

@router.post("/send/{month}")
def send_report(month: str, class_name: str = None, email: str = ADMIN_EMAIL):
    """API endpoint to send a report via email"""
    result = send_report_email(month, [email], class_name)
    return result