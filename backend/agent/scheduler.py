import os
from apscheduler.schedulers.background import BackgroundScheduler
from db.tickets import escalate_stale_tickets
from db.notifications import create_notification

ESCALATION_THRESHOLD_MINUTES = int(os.getenv("ESCALATION_THRESHOLD_MINUTES", 5))


def escalation_job():
    escalated = escalate_stale_tickets(ESCALATION_THRESHOLD_MINUTES)
    for item in escalated:
        create_notification(
            item["ticket_id"],
            "This ticket was automatically escalated to high priority because it stayed unresolved too long.",
            student_email=item.get("student_email"),
        )
    if escalated:
        print(f"[escalation] escalated tickets: {[e['ticket_id'] for e in escalated]}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(escalation_job, "interval", minutes=1, id="escalation_job")
    scheduler.start()
    return scheduler
