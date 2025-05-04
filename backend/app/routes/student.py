from fastapi import APIRouter
from app.models.student import Student
from app.config import db

router = APIRouter(prefix="/students")

@router.post("/")
def add_student(student: Student):
    db.collection("students").add(student.dict())
    return {"msg": "Student added"}
