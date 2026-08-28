import uuid
from collections import Counter
from datetime import datetime, timedelta
from db.mongo import db
from db.notifications import create_notification

tickets_collection = db["tickets"]

VALID_STATUSES = ["pending", "in_progress", "resolved"]


def create_ticket(room, block, category, priority, description, assigned_to, student_email=None):
    ticket = {
        "ticket_id": str(uuid.uuid4())[:8],
        "room": room,
        "block": block,
        "category": category,
        "priority": priority,
        "description": description,
        "assigned_to": assigned_to,
        "status": "pending",
        "escalated": False,
        "duplicate_reports": 0,
        "student_email": student_email,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    tickets_collection.insert_one(ticket)
    ticket.pop("_id", None)
    create_notification(
        ticket["ticket_id"],
        f"Ticket created for {category} issue in room {room or 'unspecified'}. Assigned to {assigned_to}.",
        student_email=student_email,
    )
    return ticket


def find_open_ticket(room, category):
    query = {"category": category, "status": {"$ne": "resolved"}}
    if room and room.lower() != "unspecified":
        query["room"] = room
    return tickets_collection.find_one(query, {"_id": 0})


def log_duplicate_report(ticket_id):
    result = tickets_collection.find_one_and_update(
        {"ticket_id": ticket_id},
        {
            "$inc": {"duplicate_reports": 1},
            "$set": {"updated_at": datetime.utcnow().isoformat()},
        },
        return_document=True,
    )
    if result:
        result.pop("_id", None)
        create_notification(
            ticket_id,
            "Another student reported the same issue. This ticket is already being tracked.",
            student_email=result.get("student_email"),
        )
    return result


def get_ticket(ticket_id):
    return tickets_collection.find_one({"ticket_id": ticket_id}, {"_id": 0})


def list_tickets(status=None, category=None, priority=None):
    query = {}
    if status:
        query["status"] = status
    if category:
        query["category"] = category
    if priority:
        query["priority"] = priority
    return list(tickets_collection.find(query, {"_id": 0}).sort("created_at", -1))


def update_ticket_status(ticket_id, new_status):
    if new_status not in VALID_STATUSES:
        return None
    result = tickets_collection.find_one_and_update(
        {"ticket_id": ticket_id},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow().isoformat()}},
        return_document=True,
    )
    if result:
        result.pop("_id", None)
        student_email = result.get("student_email")

        if new_status == "resolved":
            message = (
                f"Good news! Your ticket for the {result.get('category')} issue in room "
                f"{result.get('room') or 'unspecified'} has been marked as completed by our "
                f"maintenance team. Thank you for reporting it, and please let us know if the "
                f"issue persists."
            )
            subject = f"Ticket #{ticket_id} Resolved - HostelCare AI"
        else:
            message = f"Ticket status updated to '{new_status}'."
            subject = None

        create_notification(ticket_id, message, student_email=student_email, subject=subject)

    return result


def escalate_stale_tickets(threshold_minutes):
    cutoff_iso = (datetime.utcnow() - timedelta(minutes=threshold_minutes)).isoformat()
    stale = list(
        tickets_collection.find(
            {
                "status": {"$in": ["pending", "in_progress"]},
                "escalated": {"$ne": True},
                "created_at": {"$lt": cutoff_iso},
            }
        )
    )
    escalated = []
    for t in stale:
        tickets_collection.update_one(
            {"_id": t["_id"]},
            {
                "$set": {
                    "priority": "high",
                    "escalated": True,
                    "updated_at": datetime.utcnow().isoformat(),
                }
            },
        )
        escalated.append({"ticket_id": t["ticket_id"], "student_email": t.get("student_email")})
    return escalated


def get_analytics():
    tickets = list(tickets_collection.find({}, {"_id": 0}))

    total = len(tickets)
    by_status = Counter(t["status"] for t in tickets)
    by_category = Counter(t["category"] for t in tickets)
    by_priority = Counter(t["priority"] for t in tickets)
    by_block = Counter(t.get("block") or "Unspecified" for t in tickets)
    escalated_count = sum(1 for t in tickets if t.get("escalated"))

    room_category_pairs = Counter(
        (t.get("room") or "Unspecified", t["category"]) for t in tickets
    )
    recurring = [
        {"room": room, "category": category, "count": count}
        for (room, category), count in room_category_pairs.items()
        if count > 1
    ]
    recurring.sort(key=lambda x: x["count"], reverse=True)

    return {
        "total_tickets": total,
        "by_status": dict(by_status),
        "by_category": dict(by_category),
        "by_priority": dict(by_priority),
        "by_block": dict(by_block),
        "escalated_count": escalated_count,
        "recurring_complaints": recurring,
    }
