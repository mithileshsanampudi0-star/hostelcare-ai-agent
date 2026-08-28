from agent.groq_client import ask_groq_json

SYSTEM_PROMPT = """Determine the priority of this hostel complaint: low, medium, or high.
Rules: no water/electricity, safety hazards, or health risks = high.
Partial/intermittent issues = medium. Cosmetic/minor issues = low.
Return JSON with key: priority."""

def determine_priority(description):
    result = ask_groq_json(SYSTEM_PROMPT, description)
    return result.get("priority", "medium")
