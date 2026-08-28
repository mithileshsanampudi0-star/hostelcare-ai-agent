import React, { useState, useEffect } from "react";
import ComplaintForm from "./components/ComplaintForm";
import TicketStatus from "./components/TicketStatus";
import TicketCard from "./components/TicketCard";
import AdminDashboard from "./components/AdminDashboard";
import AdminGate from "./components/AdminGate";
import "./App.css";

function isAdminUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("admin") === "true";
}

function App() {
  const [lastResult, setLastResult] = useState(null);
  const [view, setView] = useState("submit"); // "submit" | "status"
  const [adminUnlocked, setAdminUnlocked] = useState(
    () => !!sessionStorage.getItem("hostelcare_admin_key")
  );
  const [showAdminArea, setShowAdminArea] = useState(isAdminUrl());

  useEffect(() => {
    setShowAdminArea(isAdminUrl());
  }, []);

  if (showAdminArea) {
    return (
      <div className="app app-wide">
        <header>
          <h1>🏠 HostelCare AI — Admin</h1>
        </header>
        {adminUnlocked ? (
          <AdminDashboard />
        ) : (
          <AdminGate onUnlock={() => setAdminUnlocked(true)} />
        )}
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>🏠 HostelCare AI</h1>
        <p>Intelligent Hostel Complaint Management</p>
      </header>

      <nav className="tabs">
        <button
          className={view === "submit" ? "active" : ""}
          onClick={() => setView("submit")}
        >
          Report Issue
        </button>
        <button
          className={view === "status" ? "active" : ""}
          onClick={() => setView("status")}
        >
          Check Status
        </button>
      </nav>

      <main>
        {view === "submit" && (
          <>
            <ComplaintForm onResult={setLastResult} />
            {lastResult && (
              <div className="result">
                <h3>🤖 Agent Response</h3>
                {lastResult.image_analysis && (
                  <p className="image-analysis">
                    <strong>Photo analysis:</strong> {lastResult.image_analysis}
                  </p>
                )}
                <p className="agent-message">{lastResult.agent_message}</p>
                <TicketCard ticket={lastResult.ticket} />
              </div>
            )}
          </>
        )}
        {view === "status" && <TicketStatus />}
      </main>
    </div>
  );
}

export default App;
