from fastapi import APIRouter

router = APIRouter(prefix="/students")

@router.get("/")
def list_students():
    return {"message": "List of students (stub)"}
