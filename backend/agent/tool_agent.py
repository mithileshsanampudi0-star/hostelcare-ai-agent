import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from db.tickets import find_open_ticket, create_ticket, log_duplicate_report
from db.staff import get_department_for_category

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are HostelCare AI, an intelligent hostel operations coordinator agent.

When a student reports a complaint, reason step by step and use the tools available to you:

1. Extract the room number, block, issue category, and description from the complaint.
   Valid categories: plumbing, electrical, wifi, cleaning, furniture, other.
2. Determine priority: high = no water/electricity/safety hazard, medium = partial or
   intermittent issue, low = cosmetic or minor issue.
3. ALWAYS call check_existing_ticket first, before creating anything, to see whether this
   room + category already has an open (unresolved) ticket.
4. If an open ticket already exists, call log_duplicate_report with its ticket_id instead
   of creating a new ticket. Do NOT create a duplicate.
5. If no open ticket exists, call create_ticket with the extracted details.
6. After your tool calls are done, reply with a brief, friendly 1-2 sentence message to the
   student confirming what happened, including the ticket ID.

Use "unspecified" for room or block if not mentioned in the complaint. Call exactly one of
create_ticket or log_duplicate_report per complaint - never both, never neither."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_existing_ticket",
            "description": "Check whether an open (non-resolved) ticket already exists for this room and issue category, to avoid creating a duplicate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room": {"type": "string", "description": "Room number, or 'unspecified' if not mentioned"},
                    "category": {
                        "type": "string",
                        "enum": ["plumbing", "electrical", "wifi", "cleaning", "furniture", "other"],
                    },
                },
                "required": ["room", "category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a new maintenance ticket. Only call this after confirming via check_existing_ticket that no open ticket already covers this issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room": {"type": "string", "description": "Room number, or 'unspecified'"},
                    "block": {"type": "string", "description": "Hostel block, or 'unspecified'"},
                    "category": {
                        "type": "string",
                        "enum": ["plumbing", "electrical", "wifi", "cleaning", "furniture", "other"],
                    },
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "description": {"type": "string", "description": "Clean summary of the complaint"},
                },
                "required": ["room", "block", "category", "priority", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_duplicate_report",
            "description": "Log that a student reported an issue that already has an open ticket, instead of creating a duplicate.",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "string"}},
                "required": ["ticket_id"],
            },
        },
    },
]


def _clean(value):
    if not value or value.lower() == "unspecified":
        return None
    return value


def execute_tool(name, args, student_email=None):
    if name == "check_existing_ticket":
        ticket = find_open_ticket(_clean(args.get("room")), args.get("category"))
        return ticket or {"found": False}

    if name == "create_ticket":
        room = _clean(args.get("room"))
        block = _clean(args.get("block"))
        category = args["category"]
        priority = args["priority"]
        description = args["description"]
        assigned_to = get_department_for_category(category)
        return create_ticket(
            room, block, category, priority, description, assigned_to,
            student_email=student_email,
        )

    if name == "log_duplicate_report":
        return log_duplicate_report(args["ticket_id"])

    return {"error": f"unknown tool {name}"}


def run_agent(raw_text, student_email=None, max_turns=5):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": raw_text},
    ]

    final_ticket = None

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )
        msg = response.choices[0].message

        assistant_entry = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ]
        messages.append(assistant_entry)

        if not msg.tool_calls:
            return {"agent_message": msg.content, "ticket": final_ticket}

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            result = execute_tool(name, args, student_email=student_email)
            if name in ("create_ticket", "log_duplicate_report") and result:
                final_ticket = result
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, default=str),
                }
            )

    return {"agent_message": "The agent could not finish reasoning in time.", "ticket": final_ticket}
