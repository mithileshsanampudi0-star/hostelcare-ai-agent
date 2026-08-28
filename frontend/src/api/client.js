import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

client.interceptors.request.use((config) => {
  const adminKey = sessionStorage.getItem("hostelcare_admin_key");
  if (adminKey) {
    config.headers["X-Admin-Key"] = adminKey;
  }
  return config;
});

// Complaint submission uses multipart/form-data so an image can be attached.
// We use plain axios (not the shared `client`) here so the browser sets the
// correct multipart boundary itself instead of the JSON default header.
export const submitComplaint = async ({ text, imageFile, email }) => {
  const formData = new FormData();
  if (text) formData.append("text", text);
  if (email) formData.append("email", email);
  if (imageFile) formData.append("image", imageFile);

  const res = await axios.post(`${API_BASE_URL}/api/complaint`, formData);
  return res.data; // { agent_message, ticket, image_analysis }
};

export const getTicketStatus = async (ticketId) => {
  const res = await client.get(`/api/ticket/${ticketId}`);
  return res.data;
};

export const getTicketNotifications = async (ticketId) => {
  const res = await client.get(`/api/ticket/${ticketId}/notifications`);
  return res.data;
};

export const getAllTickets = async () => {
  const res = await client.get("/api/tickets");
  return res.data;
};

// --- Admin endpoints ---

export const getAdminTickets = async (filters = {}) => {
  const params = new URLSearchParams(filters).toString();
  const res = await client.get(`/api/admin/tickets${params ? `?${params}` : ""}`);
  return res.data;
};

export const updateTicketStatus = async (ticketId, status) => {
  const res = await client.patch(`/api/admin/tickets/${ticketId}/status`, { status });
  return res.data;
};

export const getAnalytics = async () => {
  const res = await client.get("/api/admin/analytics");
  return res.data;
};

export const downloadReport = (format) => {
  const adminKey = sessionStorage.getItem("hostelcare_admin_key") || "";
  window.open(
    `${API_BASE_URL}/api/admin/report/${format}?key=${encodeURIComponent(adminKey)}`,
    "_blank"
  );
};

export const verifyAdminKey = async (key) => {
  const res = await axios.get(`${API_BASE_URL}/api/admin/analytics`, {
    headers: { "X-Admin-Key": key },
  });
  return res.data;
};

export default client;
