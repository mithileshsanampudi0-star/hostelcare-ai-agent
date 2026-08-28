from agent.groq_client import ask_groq_json

SYSTEM_PROMPT = """Classify the hostel complaint into exactly one category:
plumbing, electrical, wifi, cleaning, furniture, or other.
Return JSON with key: category."""

def classify_issue(description):
    result = ask_groq_json(SYSTEM_PROMPT, description)
    return result.get("category", "other")
