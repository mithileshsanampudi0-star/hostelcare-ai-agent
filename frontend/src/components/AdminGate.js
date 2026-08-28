import React, { useState } from "react";
import { verifyAdminKey } from "../api/client";

function AdminGate({ onUnlock }) {
  const [key, setKey] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await verifyAdminKey(key.trim());
      sessionStorage.setItem("hostelcare_admin_key", key.trim());
      onUnlock();
    } catch (err) {
      setError("Incorrect admin key.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-gate">
      <h2>🔒 Admin Access</h2>
      <p>Enter the admin key to continue.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="Admin key"
          autoFocus
        />
        <button type="submit" disabled={loading || !key.trim()}>
          {loading ? "Checking..." : "Unlock"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default AdminGate;
