import uuid
from datetime import datetime
from db.mongo import db
from services.email_service import send_email

notifications_collection = db["notifications"]


def create_notification(ticket_id, message, student_email=None, subject=None):
    note = {
        "id": str(uuid.uuid4())[:8],
        "ticket_id": ticket_id,
        "message": message,
        "created_at": datetime.utcnow().isoformat(),
    }
    notifications_collection.insert_one(note)
    note.pop("_id", None)

    if student_email:
        send_email(
            to_email=student_email,
            subject=subject or f"HostelCare Update — Ticket #{ticket_id}",
            body=message,
        )

    return note


def get_notifications_for_ticket(ticket_id):
    return list(
        notifications_collection.find({"ticket_id": ticket_id}, {"_id": 0}).sort("created_at", -1)
    )
