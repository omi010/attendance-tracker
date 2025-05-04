import pandas as pd
from app.services.email_service import send_email_alert
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def generate_monthly_absentee_report(month: str):
    # Existing code to gather absentee data

    # PDF file path
    pdf_filename = f"monthly_absentee_report_{month}.pdf"

    # Set up the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)

    # Title
    c.setFillColor(colors.blue)
    c.drawString(200, 750, f"Monthly Absentee Report - {month}")
    c.setFillColor(colors.black)
    c.drawString(200, 730, "--------------------------------------")

    # Add data to PDF with custom styling
    y_position = 700
    c.setFont("Helvetica", 12)
    for index, row in absentee_summary.iterrows():
        student_name = row['student_id']
        absentee_count = row['absentee_count']
        c.drawString(50, y_position, f"Student ID: {student_name} - Absentee Count: {absentee_count}")
        y_position -= 20

        # Alternate row colors for better readability
        if index % 2 == 0:
            c.setFillColor(colors.lightgrey)
        else:
            c.setFillColor(colors.white)

        if y_position < 100:  # Start a new page if the current one is full
            c.showPage()
            y_position = 750

    # Save PDF
    c.save()

    # Send email with the PDF attached
    subject = f"Monthly Absentee Report - {month}"
    body = f"Dear Admin,\n\nPlease find attached the absentee report for the month of {month}.\n\n" \
           f"Kind regards,\nYour Tuition Center Team"
    send_email_with_attachment(subject, body, "admin@example.com", pdf_filename)

    return absentee_summary

def generate_monthly_absentee_report(month: str):
    # Format the start and end dates for the given month
    start_date = f"{month}-01"
    end_date = f"{month}-31"  # Handle months dynamically, but we'll use this for now

    # Create an empty list to store absentee data
    absentee_data = []

    # Iterate through all the dates in the month
    for day in pd.date_range(start=start_date, end=end_date):
        date_str = day.strftime('%Y-%m-%d')

        # Get absentee data for the specific day
        attendance_ref = db.collection("attendance").document(date_str).collection("students")
        docs = attendance_ref.stream()

        for doc in docs:
            data = doc.to_dict()
            student_id = doc.id
            student = db.collection("students").document(student_id).get().to_dict()
            if student and not data.get("present", True):
                # Increment absentee count for the student
                name = student.get("name", "Student")
                absentee_data.append({
                    "name": name,
                    "student_id": student_id,
                    "date": date_str
                })

    # Create a DataFrame to aggregate the absentee count per student
    df = pd.DataFrame(absentee_data)
    absentee_summary = df.groupby("student_id").size().reset_index(name='absentee_count')

    # Generate the absentee report in Excel format
    absentee_summary.to_excel(f"monthly_absentee_report_{month}.xlsx", index=False)

    # Email the generated report to the admin
    report_path = f"monthly_absentee_report_{month}.xlsx"
    subject = f"Monthly Absentee Report - {month}"
    body = f"Attached is the absentee report for the month of {month}."
    send_email_alert(subject, body, "admin@example.com")  # Replace with admin's email

    return absentee_summary


def generate_monthly_absentee_report(month: str):
    # Existing code to gather absentee data and generate the Excel file

    # Create email content
    absentee_summary_text = f"Dear Admin,\n\nPlease find attached the absentee report for the month of {month}.\n\n" \
                            f"Summary:\n"

    for index, row in absentee_summary.iterrows():
        absentee_summary_text += f"Student: {row['student_id']}, Absentee Count: {row['absentee_count']}\n"

    absentee_summary_text += "\nKind regards,\nYour Tuition Center Team"

    # Send email with the detailed content
    subject = f"Monthly Absentee Report - {month}"
    send_email_alert(subject, absentee_summary_text, "admin@example.com")

    return absentee_summary

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_monthly_absentee_report(month: str):
    # Existing code to gather absentee data

    # PDF file path
    pdf_filename = f"monthly_absentee_report_{month}.pdf"

    # Set up the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(200, 750, f"Monthly Absentee Report - {month}")
    c.drawString(200, 730, "--------------------------------------")

    # Add data to PDF
    y_position = 700
    for index, row in absentee_summary.iterrows():
        student_name = row['student_id']
        absentee_count = row['absentee_count']
        c.drawString(50, y_position, f"Student ID: {student_name} - Absentee Count: {absentee_count}")
        y_position -= 20

        if y_position < 100:  # Start a new page if the current one is full
            c.showPage()
            y_position = 750

    # Save PDF
    c.save()

    # Send email with the PDF attached
    subject = f"Monthly Absentee Report - {month}"
    body = f"Dear Admin,\n\nPlease find attached the absentee report for the month of {month}.\n\n" \
           f"Kind regards,\nYour Tuition Center Team"

    send_email_with_attachment(subject, body, "admin@example.com", pdf_filename)

    return absentee_summary
def generate_daily_report(date: str):
    # Existing logic to retrieve attendance data for a specific day
    daily_data = retrieve_attendance_data(date)

    # Generate PDF for the daily report
    pdf_filename = f"daily_attendance_report_{date}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"Daily Attendance Report - {date}")
    c.drawString(200, 730, "--------------------------------------")

    y_position = 700
    c.setFont("Helvetica", 12)
    for index, row in daily_data.iterrows():
        student_name = row['student_id']
        status = "Present" if row['present'] else "Absent"
        c.drawString(50, y_position, f"Student ID: {student_name} - Status: {status}")
        y_position -= 20

    c.save()

    # Send email with daily report PDF
    subject = f"Daily Attendance Report - {date}"
    body = f"Dear Admin,\n\nPlease find attached the daily attendance report for {date}.\n\n" \
           f"Kind regards,\nYour Tuition Center Team"
    send_email_with_attachment(subject, body, "admin@example.com", pdf_filename)

    return daily_data

def generate_class_report(class_name: str, month: str):
    # Logic to retrieve attendance data for a specific class in a given month
    class_data = retrieve_class_attendance_data(class_name, month)

    # Generate PDF for the class report
    pdf_filename = f"{class_name}_attendance_report_{month}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"Attendance Report for {class_name} - {month}")
    c.drawString(200, 730, "--------------------------------------")

    y_position = 700
    c.setFont("Helvetica", 12)
    for index, row in class_data.iterrows():
        student_name = row['student_id']
        absentee_count = row['absentee_count']
        c.drawString(50, y_position, f"Student ID: {student_name} - Absentee Count: {absentee_count}")
        y_position -= 20

    c.save()

    # Send email with class report PDF
    subject = f"Attendance Report for {class_name} - {month}"
    body = f"Dear Admin,\n\nPlease find attached the attendance report for the class {class_name} for the month of {month}.\n\n" \
           f"Kind regards,\nYour Tuition Center Team"
    send_email_with_attachment(subject, body, "admin@example.com", pdf_filename)

    return class_data
