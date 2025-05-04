from fastapi import BackgroundTasks
import subprocess
import datetime

def schedule_weekly_training(background_tasks: BackgroundTasks):
    def train():
        print(f"[{datetime.datetime.now()}] Training AI model...")
        subprocess.run(["python", "-m", "app.services.ai_trainer"])
    background_tasks.add_task(train)
