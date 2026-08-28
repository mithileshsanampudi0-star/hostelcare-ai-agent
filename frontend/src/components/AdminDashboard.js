import React, { useEffect, useState, useCallback } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { getAdminTickets, getAnalytics, updateTicketStatus, downloadReport } from "../api/client";

const STATUS_OPTIONS = ["pending", "in_progress", "resolved"];

function toChartData(obj) {
  return Object.entries(obj || {}).map(([name, value]) => ({ name, value }));
}

function AdminDashboard() {
  const [tickets, setTickets] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [ticketData, analyticsData] = await Promise.all([
        getAdminTickets(statusFilter ? { status: statusFilter } : {}),
        getAnalytics(),
      ]);
      setTickets(ticketData);
      setAnalytics(analyticsData);
    } catch (err) {
      setError("Failed to load admin data. Is the backend running?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleStatusChange = async (ticketId, newStatus) => {
    try {
      await updateTicketStatus(ticketId, newStatus);
      loadData();
    } catch (err) {
      alert("Failed to update status.");
    }
  };

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <div className="report-buttons">
          <button onClick={() => downloadReport("csv")}>⬇ CSV Report</button>
          <button onClick={() => downloadReport("pdf")}>⬇ PDF Report</button>
        </div>
      </div>

      {error && <p className="error">{error}</p>}

      {analytics && (
        <div className="analytics-section">
          <div className="stat-cards">
            <div className="stat-card">
              <span className="stat-value">{analytics.total_tickets}</span>
              <span className="stat-label">Total Tickets</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{analytics.by_status.pending || 0}</span>
              <span className="stat-label">Pending</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{analytics.by_status.in_progress || 0}</span>
              <span className="stat-label">In Progress</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{analytics.by_status.resolved || 0}</span>
              <span className="stat-label">Resolved</span>
            </div>
          </div>

          <div className="charts-grid">
            <div className="chart-box">
              <h4>By Category</h4>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={toChartData(analytics.by_category)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#2c3e50" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-box">
              <h4>By Priority</h4>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={toChartData(analytics.by_priority)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#e67e22" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {analytics.recurring_complaints.length > 0 && (
            <div className="recurring-section">
              <h4>⚠ Recurring Complaints</h4>
              <ul>
                {analytics.recurring_complaints.map((r, i) => (
                  <li key={i}>
                    Room {r.room} — {r.category}: reported {r.count} times
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="ticket-table-section">
        <div className="table-header">
          <h3>All Tickets</h3>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">All Statuses</option>
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="ticket-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Room</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Assigned To</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((t) => (
                <tr key={t.ticket_id}>
                  <td>{t.ticket_id}</td>
                  <td>{t.room || "N/A"}</td>
                  <td>{t.category}</td>
                  <td className={`priority-${t.priority}`}>{t.priority}</td>
                  <td>{t.assigned_to}</td>
                  <td>
                    <select
                      value={t.status}
                      onChange={(e) => handleStatusChange(t.ticket_id, e.target.value)}
                    >
                      {STATUS_OPTIONS.map((s) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
