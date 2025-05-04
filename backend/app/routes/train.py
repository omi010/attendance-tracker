from fastapi import APIRouter, BackgroundTasks
from app.tasks.scheduler import schedule_weekly_training

router = APIRouter()

@router.post("/train-weekly")
def trigger_weekly_training(background_tasks: BackgroundTasks):
    schedule_weekly_training(background_tasks)
    return {"status": "Training triggered in background."}
