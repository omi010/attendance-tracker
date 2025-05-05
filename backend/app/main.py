from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.routes import student, attendance
from app.routes.auth import router as auth_router
from app.routes.report import get_monthly_summary, send_all_reports
from app.services.scheduler import start_all_schedulers
from app.services.auth import verify_password, create_access_token, get_user_from_firestore
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Routers
app.include_router(student.router)
app.include_router(attendance.router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Attendance Tracker API running"}

@app.post("/login")
@limiter.limit("5/minute")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_firestore(form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(user)}

@app.on_event("startup")
async def on_startup():
    start_all_schedulers()
