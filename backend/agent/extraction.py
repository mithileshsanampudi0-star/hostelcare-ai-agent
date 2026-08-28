from agent.groq_client import ask_groq_json

SYSTEM_PROMPT = """You extract structured info from hostel complaints.
Return JSON with keys: room (string or null), block (string or null),
issue_type (string), description (string, cleaned up summary of the complaint).
If room/block aren't mentioned, use null."""

def extract_complaint_info(raw_text):
    return ask_groq_json(SYSTEM_PROMPT, raw_text)
