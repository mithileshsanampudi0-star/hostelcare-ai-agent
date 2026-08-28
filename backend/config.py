import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hostelcare")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_VISION_MODEL = "qwen/qwen3.6-27b"

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "hostelcare-admin-2026")

# SMTP settings for email notifications. Leave blank to run in simulated mode
# (emails get printed to the backend console instead of actually sent) -
# useful while you don't have real credentials yet.
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "HostelCare AI")
