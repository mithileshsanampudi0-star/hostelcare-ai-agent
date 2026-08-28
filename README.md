# 🏠 HostelCare AI Agent

An intelligent **AI-powered hostel complaint management system** that automatically understands student complaints, classifies issues, assigns them to the appropriate department, prioritizes tickets, detects duplicate complaints, and sends email notifications.

---

## 🚀 Features

### 🤖 AI-Powered Complaint Processing

* Natural-language complaint understanding
* Automatic extraction of:

  * Room number
  * Hostel block
  * Complaint category
  * Issue description
* AI-based priority classification:

  * 🔴 High
  * 🟡 Medium
  * 🟢 Low

### 🎫 Smart Ticket Management

* Automatically creates maintenance tickets
* Generates unique ticket IDs
* Tracks ticket status:

  * Pending
  * In Progress
  * Resolved
* Prevents duplicate tickets for the same room and issue
* Tracks duplicate reports

### 🧠 AI Agent System

HostelCare uses an agent-based workflow to process complaints.

```text
Student Complaint
       ↓
   AI Extraction
       ↓
   Classification
       ↓
 Priority Analysis
       ↓
Duplicate Detection
       ↓
Ticket Creation
       ↓
Department Assignment
       ↓
Email Notification
```

### 📧 Email Notifications

HostelCare uses **Resend API** for email notifications.

Emails can be sent when:

* A ticket is created
* A duplicate complaint is reported
* A ticket is resolved
* A ticket is automatically escalated

For development/testing, the application supports simulated email output when `RESEND_API_KEY` is not configured.

### ⏫ Automatic Escalation

Unresolved tickets are periodically checked by the scheduler.

If a ticket remains unresolved beyond the configured threshold:

```text
Pending Ticket
      ↓
Time Threshold Exceeded
      ↓
Priority → HIGH
      ↓
Escalated → TRUE
      ↓
Student Notification
```

### 🖼️ Image Complaint Support

Students can attach images to complaints.

Supported formats:

* JPEG
* PNG
* WEBP

Maximum image size:

```text
8 MB
```

The AI vision system analyzes the uploaded image and includes the analysis with the complaint.

### 📊 Admin Dashboard

Administrators can view:

* Total tickets
* Ticket status
* Complaint categories
* Priority distribution
* Hostel block statistics
* Escalated tickets
* Recurring complaints

---

# 🛠️ Tech Stack

## Frontend

* React
* JavaScript
* Axios
* CSS

## Backend

* Python
* Flask
* Flask-CORS
* Gunicorn

## AI

* Groq API
* `openai/gpt-oss-120b`
* `qwen/qwen3.6-27b`
* AI tool calling
* AI agent workflow

## Database

* MongoDB Atlas
* PyMongo

## Email

* Resend API

## Other

* APScheduler
* Requests
* Python-dotenv

## Deployment

* GitHub
* Render

---

# 📁 Project Structure

```text
Hostelcare/
│
├── backend/
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── assignment.py
│   │   ├── classification.py
│   │   ├── extraction.py
│   │   ├── graph.py
│   │   ├── groq_client.py
│   │   ├── priority.py
│   │   ├── scheduler.py
│   │   ├── tool_agent.py
│   │   └── vision.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── mongo.py
│   │   ├── notifications.py
│   │   ├── staff.py
│   │   └── tickets.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   ├── complaint_routes.py
│   │   └── ticket_routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py
│   │
│   ├── scripts/
│   │   └── seed_staff.py
│   │
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── package-lock.json
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/mithileshsanampudi0-star/hostelcare-ai-agent.git
cd hostelcare-ai-agent
```

---

# 🐍 Backend Setup

Go to the backend directory:

```bash
cd backend
```

Create a virtual environment:

### Windows

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
GROQ_API_KEY=your_groq_api_key

MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

MONGO_DB_NAME=hostelcare

ADMIN_API_KEY=your_admin_api_key

RESEND_API_KEY=your_resend_api_key

EMAIL_FROM=HostelCare <onboarding@resend.dev>

ESCALATION_THRESHOLD_MINUTES=5
```

### ⚠️ Important

Never commit `.env` to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
venv/
__pycache__/
*.pyc
node_modules/
build/
```

---

# 🗄️ MongoDB Atlas

HostelCare uses MongoDB Atlas for production.

Create a MongoDB Atlas cluster and obtain the connection string.

Set:

```env
MONGO_URI=your_mongodb_atlas_connection_string
```

Also make sure your MongoDB Atlas network access allows the Render service to connect.

---

# ▶️ Run Backend

From:

```text
Hostelcare/backend
```

run:

```cmd
python app.py
```

Backend:

```text
http://localhost:5000
```

Health check:

```text
http://localhost:5000/
```

Expected response:

```json
{
  "status": "HostelCare AI backend running"
}
```

---

# ⚛️ Frontend Setup

Open another terminal.

From the project root:

```cmd
cd frontend
```

Install dependencies:

```cmd
npm install
```

Start React:

```cmd
npm start
```

Frontend:

```text
http://localhost:3000
```

---

# 🔗 Frontend API Configuration

The frontend uses an environment variable for the backend URL.

Example:

```javascript
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000";
```

For local development:

```text
http://localhost:5000
```

For production:

```env
REACT_APP_API_URL=https://hostelcare-ai-agent.onrender.com
```

---

# 📡 API Endpoints

## Submit Complaint

```http
POST /api/complaint
```

Supports:

* JSON requests
* Multipart form requests
* Optional image upload
* Optional student email

---

## Ticket APIs

```text
/api/tickets
```

Used for retrieving and managing tickets.

---

## Admin APIs

```text
/api/admin/...
```

Used by the administrator dashboard.

---

# 📧 Email Configuration

HostelCare uses Resend instead of SMTP.

Required environment variables:

```env
RESEND_API_KEY=your_resend_api_key
EMAIL_FROM=HostelCare <onboarding@resend.dev>
```

For testing, `onboarding@resend.dev` can be used with Resend's testing restrictions.

For production email delivery to arbitrary student addresses, verify your own domain in Resend and use an address such as:

```env
EMAIL_FROM=HostelCare <notifications@yourdomain.com>
```

---

# 🌐 Deployment on Render

HostelCare is deployed as two separate Render services.

## Backend

### Root Directory

```text
backend
```

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Environment Variables

Configure these in Render:

```text
GROQ_API_KEY
MONGO_URI
MONGO_DB_NAME
ADMIN_API_KEY
RESEND_API_KEY
EMAIL_FROM
ESCALATION_THRESHOLD_MINUTES
```

Backend URL:

```text
https://hostelcare-ai-agent.onrender.com
```

---

# Frontend Deployment

Create a Render **Static Site**.

### Root Directory

```text
frontend
```

### Build Command

```bash
npm install && npm run build
```

### Publish Directory

```text
build
```

### Environment Variable

```text
REACT_APP_API_URL=https://hostelcare-ai-agent.onrender.com
```

After changing `REACT_APP_API_URL`, rebuild the frontend because React environment variables are included during the production build.

---

# 🔄 Production Architecture

```text
                    ┌─────────────────────┐
                    │      Student        │
                    │   React Frontend    │
                    └──────────┬──────────┘
                               │
                               │ HTTPS
                               ▼
              ┌────────────────────────────┐
              │      Render Frontend       │
              │      React Static Site     │
              └──────────────┬─────────────┘
                             │
                             │ REST API
                             ▼
              ┌────────────────────────────┐
              │      Render Backend        │
              │       Flask + Gunicorn     │
              └──────┬─────────┬───────────┘
                     │         │
          ┌──────────┘         └───────────┐
          ▼                                ▼
 ┌──────────────────┐             ┌──────────────────┐
 │   MongoDB Atlas  │             │     Groq API     │
 │     Database     │             │    AI Models     │
 └──────────────────┘             └──────────────────┘
                     │
                     ▼
             ┌──────────────────┐
             │    Resend API    │
             │ Email Notification│
             └──────────────────┘
```

---

# 🔒 Security

Do not expose these values publicly:

```text
GROQ_API_KEY
MONGO_URI
RESEND_API_KEY
ADMIN_API_KEY
```

Keep them inside:

```text
.env
```

for local development and Render Environment Variables for production.

Never commit API keys to GitHub.

If a secret is accidentally committed, revoke it and generate a new one.

---

# 🧪 Testing

Test the backend health endpoint:

```text
GET /
```

Expected:

```json
{
  "status": "HostelCare AI backend running"
}
```

Test complaint submission from the React frontend.

Verify:

1. Complaint reaches Flask backend.
2. AI processes the complaint.
3. Ticket is created.
4. Ticket appears in MongoDB Atlas.
5. Correct department is assigned.
6. Email notification is generated/sent.
7. Duplicate complaints do not create duplicate tickets.
8. Stale tickets are escalated.

---

# 📈 Future Improvements

* Student authentication
* Admin authentication with role-based access
* Real-time ticket updates
* WhatsApp notifications
* SMS notifications
* Hostel-wise analytics
* Maintenance staff mobile application
* Better AI-based image diagnosis
* Complaint sentiment analysis
* SLA monitoring
* Advanced analytics dashboard

---

# 👨‍💻 Author

**Mithilesh Sanampudi**

GitHub:

```text
https://github.com/mithileshsanampudi0-star
```

Project:

```text
https://github.com/mithileshsanampudi0-star/hostelcare-ai-agent
```

---

# 📄 License

This project is developed for educational and project demonstration purposes.
