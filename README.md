# 🏠 HostelCare AI

**Intelligent Hostel Operations & Complaint Management Agent**

HostelCare AI is an agentic system that lets students report hostel maintenance issues in
plain language (text and/or a photo), and has an LLM-powered agent reason through what to
do next — check for duplicates, classify and prioritize the issue, assign it to the right
team, create a ticket, and keep the student updated — instead of following a fixed,
hardcoded pipeline.

---

## Table of Contents

- [Why This Is an Agent, Not Just a Script](#why-this-is-an-agent-not-just-a-script)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [Admin Access](#admin-access)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

---

## Why This Is an Agent, Not Just a Script

Most "AI agent" projects run every input through the same fixed sequence of steps, every
time — extract, then classify, then prioritize, then assign, in that exact order. That's
automation *with* an LLM call inside it, not really an agent.

HostelCare AI's core complaint handler works differently. The LLM is given a set of tools
(`check_existing_ticket`, `create_ticket`, `log_duplicate_report`) and reasons through the
situation itself, deciding at runtime:

```
Complaint text/photo
        │
        ▼
LLM extracts room, block, category, priority from the complaint
        │
        ▼
LLM calls check_existing_ticket(room, category)
        │
        ├── Open ticket already exists?
        │        │
        │        ▼
        │   LLM calls log_duplicate_report(ticket_id)
        │
        └── No open ticket?
                 │
                 ▼
            LLM calls create_ticket(...)
        │
        ▼
LLM writes a natural-language reply to the student
```

The sequence of actions isn't hardcoded — the model decides whether to log a duplicate or
create a new ticket based on what it actually finds when it checks. This is what lets the
system genuinely prevent duplicate complaints (a challenge explicitly named in the
original problem brief) instead of just recording every report as a new ticket.

---

## Features

- **Natural language complaint intake** — students describe issues conversationally, no
  forms or dropdowns
- **Photo support** — attach a photo of the issue; a vision-capable LLM describes what's
  wrong and folds that into the same reasoning pipeline
- **Automatic categorization & prioritization** — plumbing, electrical, wifi, cleaning,
  furniture, or other; priority determined by urgency/safety rules
- **Duplicate detection** — the agent checks for an existing open ticket on the same
  room + category before creating a new one
- **Automatic team assignment** — tickets are routed to the right maintenance department
- **Ticket tracking** — students can check status any time by ticket ID
- **Automated escalation** — a background job bumps stale, unresolved tickets to high
  priority on its own schedule
- **Notifications** — in-app notification history per ticket, plus optional email updates
  (falls back to a simulated console log if SMTP isn't configured)
- **Admin dashboard** — live ticket table with filters and inline status updates, protected
  behind a secret-key gate (not visible in normal student navigation)
- **Analytics** — counts by status/category/priority/block, plus automatic detection of
  recurring complaints (same room + category reported more than once)
- **Reports** — downloadable CSV and formatted PDF summaries for hostel administration

---

## Architecture

```
┌─────────────┐        ┌──────────────────┐        ┌─────────────┐
│   React     │  HTTP  │   Flask Backend   │        │   MongoDB   │
│  Frontend   │◄──────►│                   │◄──────►│             │
└─────────────┘        │  ┌─────────────┐  │        └─────────────┘
                        │  │ Tool-Calling │  │
                        │  │    Agent     │──┼──► Groq API (LLM + Vision)
                        │  └─────────────┘  │
                        │  ┌─────────────┐  │
                        │  │  Scheduler   │──┼──► Escalation job (every 1 min)
                        │  └─────────────┘  │
                        │  ┌─────────────┐  │
                        │  │Email Service │──┼──► SMTP (or simulated console log)
                        │  └─────────────┘  │
                        └───────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM / Reasoning | Groq API (`openai/gpt-oss-120b`) |
| Vision (photo analysis) | Groq API (`qwen/qwen3.6-27b`) |
| Agent orchestration | Custom tool-calling loop (function calling) |
| Backend | Flask, Flask-CORS |
| Database | MongoDB (via PyMongo) |
| Background jobs | APScheduler |
| PDF reports | fpdf2 |
| Email | Python `smtplib` (stdlib, no external dependency) |
| Frontend | React (Create React App) |
| Charts | Recharts |

---

## Project Structure

```
Hostelcare/
├── backend/
│   ├── app.py                     # Flask entry point, registers blueprints + scheduler
│   ├── config.py                  # env vars: Groq/SMTP/Mongo/admin settings
│   ├── .env
│   ├── requirements.txt
│   │
│   ├── agent/
│   │   ├── tool_agent.py          # Core agentic loop (tool-calling reasoning)
│   │   ├── vision.py              # Photo analysis via Groq vision model
│   │   └── scheduler.py           # Background escalation job
│   │
│   ├── db/
│   │   ├── mongo.py               # MongoDB connection
│   │   ├── tickets.py             # Ticket CRUD, duplicate detection, analytics
│   │   ├── staff.py                # Department lookup + staff seeding
│   │   └── notifications.py       # Notification log + email dispatch
│   │
│   ├── services/
│   │   └── email_service.py       # SMTP sending with simulated fallback
│   │
│   ├── routes/
│   │   ├── complaint_routes.py    # POST /api/complaint (agent entry point)
│   │   ├── ticket_routes.py       # GET ticket status + notifications
│   │   └── admin_routes.py        # Admin ticket list, analytics, reports (key-protected)
│   │
│   └── scripts/
│       └── seed_staff.py
│
└── frontend/
    └── src/
        ├── App.js                  # Tab navigation + admin URL gate
        ├── App.css
        ├── api/
        │   └── client.js           # API wrapper (axios)
        └── components/
            ├── ComplaintForm.js     # Text + photo + email submission
            ├── TicketCard.js
            ├── TicketStatus.js      # Status lookup + notification history
            ├── AdminGate.js         # PIN entry for admin access
            └── AdminDashboard.js    # Stats, charts, ticket table, report downloads
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- MongoDB running locally (or a connection string to a hosted instance)
- A [Groq API key](https://console.groq.com)

### Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/seed_staff.py
```

### Frontend

```bash
cd frontend
npm install
```

---

## Environment Variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=hostelcare
FLASK_PORT=5000

ADMIN_API_KEY=change-this-to-something-private
ESCALATION_THRESHOLD_MINUTES=4320

# Leave blank to run emails in simulated mode (printed to console).
# For Gmail: generate an App Password at myaccount.google.com/apppasswords
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_NAME=HostelCare AI
```

> **Note:** `ESCALATION_THRESHOLD_MINUTES` controls how long a ticket can sit unresolved
> before being auto-escalated to high priority. `4320` = 3 days, suitable for production.
> Lower it (e.g. `2`) temporarily if you want to demo escalation live.

---

## Running the App

**Terminal 1 — backend:**
```bash
cd backend
python app.py
```
Runs on `http://localhost:5000`

**Terminal 2 — frontend:**
```bash
cd frontend
npm start
```
Runs on `http://localhost:3000`

---

## API Reference

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/complaint` | Submit a complaint (text and/or photo, optional email) → agent reasons and creates/updates a ticket |
| `GET` | `/api/ticket/<id>` | Get a ticket's current status |
| `GET` | `/api/ticket/<id>/notifications` | Get the notification history for a ticket |
| `GET` | `/api/tickets` | List all tickets |
| `GET` | `/api/admin/tickets` | *(admin key required)* Filterable ticket list |
| `PATCH` | `/api/admin/tickets/<id>/status` | *(admin key required)* Update ticket status |
| `GET` | `/api/admin/analytics` | *(admin key required)* Aggregated stats + recurring complaints |
| `GET` | `/api/admin/report/csv` | *(admin key required)* Download all tickets as CSV |
| `GET` | `/api/admin/report/pdf` | *(admin key required)* Download a formatted PDF report |

Admin routes require an `X-Admin-Key` header (or `?key=` query param for file downloads)
matching `ADMIN_API_KEY` in `.env`.

### Example: submit a complaint

```bash
curl -X POST http://localhost:5000/api/complaint \
  -H "Content-Type: application/json" \
  -d '{"text": "Bathroom tap in room 204 has been leaking for 3 days"}'
```

---

## Admin Access

The admin dashboard is intentionally **not** linked anywhere in normal student navigation.
Access it at:

```
http://localhost:3000/?admin=true
```

You'll be prompted for the admin key (set via `ADMIN_API_KEY` in `.env`). This key is
validated against the real backend — every `/api/admin/*` route rejects requests without
it, so hiding the UI tab isn't the only protection; the API itself is gated too.

---

## Known Limitations

This is a hackathon/bootcamp-stage MVP. Before any real deployment, it would need:

- **Proper student authentication** — currently there's no login system; email is
  optionally self-reported per complaint for notifications
- **Rate limiting** — no protection against spam/abuse on the complaint endpoint
- **Multi-tenant support** — currently modeled for a single hostel; multiple
  hostels/campuses would need tenant isolation
- **Persistent admin sessions** — the admin key is stored in `sessionStorage`, cleared on
  browser close, with no refresh/rotation mechanism

---

## Future Improvements

- Real-time push notifications (not just email)
- Multi-language complaint support
- Predictive maintenance using recurring-complaint patterns to flag at-risk
  rooms/blocks before failures occur
- Mobile app / PWA for easier student access

---

## Credits

Built for the AI Agent Bootcamp — Smart Hostel Management Agent problem statement.

Powered by [Groq](https://groq.com) for fast LLM inference and vision.
