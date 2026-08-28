import csv
import io
from functools import wraps
from flask import Blueprint, request, jsonify, Response, send_file
from config import ADMIN_API_KEY
from db.tickets import list_tickets, update_ticket_status, get_analytics

admin_bp = Blueprint("admin", __name__)


def require_admin_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get("X-Admin-Key") or request.args.get("key")
        if provided_key != ADMIN_API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route("/api/admin/tickets", methods=["GET"])
@require_admin_key
def admin_list_tickets():
    status = request.args.get("status")
    category = request.args.get("category")
    priority = request.args.get("priority")
    tickets = list_tickets(status=status, category=category, priority=priority)
    return jsonify(tickets)


@admin_bp.route("/api/admin/tickets/<ticket_id>/status", methods=["PATCH"])
@require_admin_key
def admin_update_status(ticket_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    updated = update_ticket_status(ticket_id, new_status)
    if not updated:
        return jsonify({"error": "Invalid ticket_id or status"}), 400
    return jsonify(updated)


@admin_bp.route("/api/admin/analytics", methods=["GET"])
@require_admin_key
def admin_analytics():
    return jsonify(get_analytics())


@admin_bp.route("/api/admin/report/csv", methods=["GET"])
@require_admin_key
def admin_report_csv():
    tickets = list_tickets()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Ticket ID", "Room", "Block", "Category", "Priority",
        "Status", "Assigned To", "Description", "Created At", "Updated At"
    ])
    for t in tickets:
        writer.writerow([
            t.get("ticket_id"), t.get("room"), t.get("block"),
            t.get("category"), t.get("priority"), t.get("status"),
            t.get("assigned_to"), t.get("description"),
            t.get("created_at"), t.get("updated_at"),
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=hostelcare_report.csv"},
    )


def _safe(value, max_word_len=30):
    """Make any string safe to print in the PDF:
    1. FPDF's core Helvetica font only supports latin-1, so strip/replace
       anything outside that range (emoji, smart quotes, em-dashes, etc.)
       coming from user text or LLM-generated text.
    2. FPDF can't wrap a single "word" (whitespace-free run of characters)
       that's wider than the page - it just crashes. Force-break any run
       longer than max_word_len so it always has somewhere to wrap,
       regardless of what a student typed or the LLM extracted.
    """
    if value is None:
        return ""
    text = str(value)
    text = text.encode("latin-1", errors="replace").decode("latin-1")

    broken_words = []
    for word in text.split(" "):
        while len(word) > max_word_len:
            broken_words.append(word[:max_word_len])
            word = word[max_word_len:]
        broken_words.append(word)
    return " ".join(broken_words)


@admin_bp.route("/api/admin/report/pdf", methods=["GET"])
@require_admin_key
def admin_report_pdf():
    from fpdf import FPDF

    tickets = list_tickets()
    analytics = get_analytics()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _safe("HostelCare AI - Maintenance Report"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, _safe(f"Total Tickets: {analytics['total_tickets']}"), ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _safe("Summary by Status"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    for status, count in analytics["by_status"].items():
        pdf.cell(0, 6, _safe(f"  {status}: {count}"), ln=True)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _safe("Summary by Category"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    for category, count in analytics["by_category"].items():
        pdf.cell(0, 6, _safe(f"  {category}: {count}"), ln=True)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _safe("Recurring Complaints"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    if analytics["recurring_complaints"]:
        for r in analytics["recurring_complaints"]:
            pdf.cell(0, 6, _safe(f"  Room {r['room']} - {r['category']}: {r['count']} times"), ln=True)
    else:
        pdf.cell(0, 6, _safe("  None detected"), ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _safe("All Tickets"), ln=True)
    pdf.set_font("Helvetica", "", 8)
    for t in tickets:
        line = _safe(
            f"[{t.get('ticket_id')}] Room {t.get('room')} | {t.get('category')} | "
            f"{t.get('priority')} | {t.get('status')}"
        )
        # Use cell() instead of multi_cell(): these lines are always short
        # enough to fit on one row, and this sidesteps a known fpdf2 bug where
        # multi_cell's automatic line-wrapping can throw a spurious
        # "Not enough horizontal space" error even on text that fits fine.
        # Truncate defensively in case a field is ever unexpectedly long.
        line = line[:110]
        pdf.cell(0, 5, line, ln=True)

    pdf_bytes = bytes(pdf.output())
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="hostelcare_report.pdf",
    )