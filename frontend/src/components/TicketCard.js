import React from "react";

const priorityColors = {
  high: "#e74c3c",
  medium: "#f39c12",
  low: "#27ae60",
};

function TicketCard({ ticket }) {
  if (!ticket) return null;

  return (
    <div className="ticket-card">
      <div className="ticket-header">
        <span className="ticket-id">#{ticket.ticket_id}</span>
        <span
          className="priority-badge"
          style={{ backgroundColor: priorityColors[ticket.priority] || "#999" }}
        >
          {ticket.priority}
        </span>
      </div>
      {ticket.escalated && <p className="flag flag-escalated">⚠ Escalated</p>}
      {ticket.duplicate_reports > 0 && (
        <p className="flag flag-duplicate">
          🔁 Reported {ticket.duplicate_reports + 1} time(s)
        </p>
      )}
      <p><strong>Category:</strong> {ticket.category}</p>
      <p><strong>Room:</strong> {ticket.room || "N/A"} {ticket.block ? `(Block ${ticket.block})` : ""}</p>
      <p><strong>Description:</strong> {ticket.description}</p>
      <p><strong>Assigned to:</strong> {ticket.assigned_to}</p>
      <p><strong>Status:</strong> {ticket.status}</p>
    </div>
  );
}

export default TicketCard;
