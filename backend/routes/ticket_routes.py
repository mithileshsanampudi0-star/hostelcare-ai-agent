from flask import Blueprint, jsonify
from db.tickets import get_ticket, list_tickets
from db.notifications import get_notifications_for_ticket

ticket_bp = Blueprint("ticket", __name__)


@ticket_bp.route("/api/ticket/<ticket_id>", methods=["GET"])
def get_ticket_status(ticket_id):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(ticket)


@ticket_bp.route("/api/ticket/<ticket_id>/notifications", methods=["GET"])
def ticket_notifications(ticket_id):
    return jsonify(get_notifications_for_ticket(ticket_id))


@ticket_bp.route("/api/tickets", methods=["GET"])
def get_all_tickets():
    return jsonify(list_tickets())
