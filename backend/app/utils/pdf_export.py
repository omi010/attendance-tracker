# backend/app/utils/pdf_export.py
import pdfkit

def generate_pdf_report(html_string: str, filename="attendance_report.pdf"):
    file_path = f"reports/{filename}"
    pdfkit.from_string(html_string, file_path)
    return file_path

html = """
<h1>Monthly Attendance Report</h1>
<table>
  <tr><th>Student</th><th>Days Present</th></tr>
  <tr><td>abc123</td><td>20</td></tr>
</table>
"""
