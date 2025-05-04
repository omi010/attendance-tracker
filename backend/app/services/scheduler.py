from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from app.routes.report import email_absentee_parents
from app.routes.report import check_absentee_alert
from datetime import datetime
from app.services.report_generator import generate_monthly_absentee_report

def send_daily_absentee_alerts():
    # Format current date in 'YYYY-MM-DD' format
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Run absentee email function
    email_absentee_parents(today_date)

    # Run absentee threshold alert (if over a certain number of absentees)
    check_absentee_alert(today_date, threshold=10)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_absentee_alerts, 'interval', hours=24, start_date='2025-05-04 18:00:00')
    scheduler.start()

    # Optional: Listen to job events (to log success/failures)
    def job_listener(event):
        if event.exception:
            print(f"Job {event.job_id} failed!")
        else:
            print(f"Job {event.job_id} completed successfully.")

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


def send_monthly_report():
    current_month = datetime.today().strftime('%Y-%m')
    generate_monthly_absentee_report(current_month)


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Schedule monthly report generation on the last day of the month at 6 PM
    scheduler.add_job(send_monthly_report, 'cron', day='last', hour=18, minute=0)

    scheduler.start()


def send_monthly_report():
    current_month = datetime.today().strftime('%Y-%m')
    generate_monthly_absentee_report(current_month)


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Schedule monthly report generation on the last day of the month at 6 PM
    scheduler.add_job(send_monthly_report, 'cron', day='last', hour=18, minute=0)

    scheduler.start()

def start_alert_scheduler():
    scheduler = BackgroundScheduler()

    # Check for high absentee counts every day at 10 AM
    scheduler.add_job(check_for_high_absentee_counts, 'cron', hour=10, minute=0)

    scheduler.start()
