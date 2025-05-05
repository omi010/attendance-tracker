from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/me")
def get_me():
    return {"message": "User profile (stub)"}
