from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.routes.report import send_all_reports
from app.routes.attendance import check_for_high_absentee_counts
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.routes.report import send_all_reports
from app.routes.attendance import check_for_high_absentee_counts
from app.services.ai_trainer import train_model

def start_email_scheduler():
    """Start scheduler for sending reports on the first day of each month"""
    scheduler = BackgroundScheduler()
    # Send reports at 9 AM on the first day of each month
    scheduler.add_job(
        lambda: send_all_reports(datetime.now().strftime("%Y-%m")), 
        'cron', 
        day=1, 
        hour=9
    )
    scheduler.start()
    print("✅ Email scheduler started")

def start_alert_scheduler():
    """Start scheduler for checking high absentee counts daily"""
    scheduler = BackgroundScheduler()
    # Check absentees at 10 AM every day
    scheduler.add_job(
        check_for_high_absentee_counts, 
        'cron', 
        hour=10, 
        minute=0
    )
    scheduler.start()
    print("✅ Alert scheduler started")

def start_model_training_scheduler():
    """Start scheduler for retraining the prediction model weekly"""
    scheduler = BackgroundScheduler()
    # Retrain model at 1 AM every Sunday
    scheduler.add_job(
        train_model, 
        'cron', 
        day_of_week=6, 
        hour=1
    )
    scheduler.start()
    print("✅ Model training scheduler started")
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from app.config import APP_ENV, RETRAIN_MODEL_WEEKLY

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize a single scheduler instance
scheduler = BackgroundScheduler()

def start_email_scheduler():
    """Start scheduler for sending reports on the first day of each month"""
    from app.routes.report import send_all_reports
    
    # Get current month in YYYY-MM format
    current_month = datetime.now().strftime("%Y-%m")
    
    try:
        # Send reports at 9 AM on the first day of each month
        scheduler.add_job(
            lambda: send_all_reports(current_month), 
            'cron', 
            day=1, 
            hour=9,
            id='monthly_report_job',
            replace_existing=True
        )
        logger.info("✅ Email scheduler started")
    except Exception as e:
        logger.error(f"❌ Error starting email scheduler: {str(e)}")

def start_alert_scheduler():
    """Start scheduler for checking high absentee counts daily"""
    from app.routes.attendance import check_for_high_absentee_counts
    
    try:
        # Check absentees at 10 AM every day
        scheduler.add_job(
            check_for_high_absentee_counts, 
            'cron', 
            hour=10, 
            minute=0,
            id='absentee_check_job',
            replace_existing=True
        )
        logger.info("✅ Alert scheduler started")
    except Exception as e:
        logger.error(f"❌ Error starting alert scheduler: {str(e)}")

def start_model_training_scheduler():
    """Start scheduler for retraining the prediction model weekly"""
    from app.services.ai_trainer import train_model
    
    if not RETRAIN_MODEL_WEEKLY:
        logger.info("⏭ Model training scheduler skipped (disabled in config)")
        return
    
    try:
        # Retrain model at 1 AM every Sunday
        scheduler.add_job(
            train_model, 
            'cron', 
            day_of_week=6, 
            hour=1,
            id='model_training_job',
            replace_existing=True
        )
        logger.info("✅ Model training scheduler started")
    except Exception as e:
        logger.error(f"❌ Error starting model training scheduler: {str(e)}")

def start_daily_reminder_scheduler():
    """Start scheduler for sending daily reminders"""
    from app.services.emailer import send_daily_absentee_alerts
    
    try:
        # Send reminders at 8 AM on weekdays
        scheduler.add_job(
            send_daily_absentee_alerts,
            'cron',
            day_of_week='mon-fri',
            hour=8,
            id='daily_reminder_job',
            replace_existing=True
        )
        logger.info("✅ Daily reminder scheduler started")
    except Exception as e:
        logger.error(f"❌ Error starting daily reminder scheduler: {str(e)}")

def start_all_schedulers():
    """Start all scheduler processes"""
    try:
        # Only start schedulers in production mode if needed
        if APP_ENV == "development" and os.getenv("DISABLE_SCHEDULERS", "False").lower() in ["true", "1", "t"]:
            logger.info("⏭ Schedulers disabled in development mode")
            return
            
        # Start individual schedulers
        start_email_scheduler()
        start_alert_scheduler()
        start_model_training_scheduler()
        start_daily_reminder_scheduler()
        
        # Start the scheduler if not already running
        if not scheduler.running:
            scheduler.start()
            
        logger.info("✅ All schedulers started successfully")
    except Exception as e:
        logger.error(f"❌ Error starting schedulers: {str(e)}")

def shutdown_schedulers():
    """Shutdown all schedulers"""
    try:
        if scheduler.running:
            scheduler.shutdown()
        logger.info("✅ All schedulers shut down")
    except Exception as e:
        logger.error(f"❌ Error shutting down schedulers: {str(e)}")
def start_all_schedulers():
    """Start all scheduler processes"""
    start_email_scheduler()
    start_alert_scheduler()
    start_model_training_scheduler()
    print("✅ All schedulers started successfully")
def start_all_schedulers():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_high_absentee_counts, 'cron', hour=10)
    scheduler.add_job(lambda: send_all_reports(datetime.now().strftime("%Y-%m")), 'cron', day=1, hour=9)
    scheduler.start()
