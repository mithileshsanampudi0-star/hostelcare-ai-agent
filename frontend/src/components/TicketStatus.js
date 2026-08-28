import React, { useState } from "react";
import { getTicketStatus, getTicketNotifications } from "../api/client";
import TicketCard from "./TicketCard";

function TicketStatus() {
  const [ticketId, setTicketId] = useState("");
  const [ticket, setTicket] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!ticketId.trim()) return;

    setLoading(true);
    setError(null);
    setTicket(null);
    setNotifications([]);
    try {
      const [ticketData, notifData] = await Promise.all([
        getTicketStatus(ticketId.trim()),
        getTicketNotifications(ticketId.trim()),
      ]);
      setTicket(ticketData);
      setNotifications(notifData);
    } catch (err) {
      setError("Ticket not found.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ticket-status">
      <h2>Check Ticket Status</h2>
      <form onSubmit={handleCheck}>
        <input
          type="text"
          value={ticketId}
          onChange={(e) => setTicketId(e.target.value)}
          placeholder="Enter ticket ID"
        />
        <button type="submit" disabled={loading}>
          {loading ? "Checking..." : "Check"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {ticket && <TicketCard ticket={ticket} />}

      {notifications.length > 0 && (
        <div className="notifications-list">
          <h4>Updates</h4>
          <ul>
            {notifications.map((n) => (
              <li key={n.id}>
                <span className="notif-time">
                  {new Date(n.created_at).toLocaleString()}
                </span>
                <span className="notif-message">{n.message}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TicketStatus;
