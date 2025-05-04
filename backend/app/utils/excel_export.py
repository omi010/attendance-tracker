# backend/app/utils/excel_export.py
import pandas as pd

def generate_excel_report(data: list, filename="attendance_report.xlsx"):
    """
    data: List of dicts, e.g. [{"student_id": "abc123", "present_days": 20}, ...]
    filename: Name of the Excel file to create
    """
    df = pd.DataFrame(data)
    file_path = f"reports/{filename}"
    df.to_excel(file_path, index=False)
    return file_path

def generate_excel_report(data: list, filename: str) -> str:
    df = pd.DataFrame(data)
    filepath = f"/tmp/{filename}"
    df.to_excel(filepath, index=False)
    return filepath
