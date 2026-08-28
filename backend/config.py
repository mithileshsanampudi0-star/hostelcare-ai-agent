import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "hostelcare"
)

FLASK_PORT = int(
    os.getenv("PORT", os.getenv("FLASK_PORT", 5000))
)

GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_VISION_MODEL = "qwen/qwen3.6-27b"

ADMIN_API_KEY = os.getenv(
    "ADMIN_API_KEY",
    "hostelcare-admin-2026"
)
