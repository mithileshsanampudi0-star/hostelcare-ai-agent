from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agent.extraction import extract_complaint_info
from agent.classification import classify_issue
from agent.priority import determine_priority
from agent.assignment import assign_team
from db.tickets import create_ticket


class ComplaintState(TypedDict):
    raw_text: str
    room: Optional[str]
    block: Optional[str]
    description: Optional[str]
    category: Optional[str]
    priority: Optional[str]
    assigned_to: Optional[str]
    ticket: Optional[dict]


def extract_node(state: ComplaintState):
    info = extract_complaint_info(state["raw_text"])
    return {
        "room": info.get("room"),
        "block": info.get("block"),
        "description": info.get("description", state["raw_text"]),
    }


def classify_node(state: ComplaintState):
    return {"category": classify_issue(state["description"])}


def priority_node(state: ComplaintState):
    return {"priority": determine_priority(state["description"])}


def assign_node(state: ComplaintState):
    return {"assigned_to": assign_team(state["category"])}


def ticket_node(state: ComplaintState):
    ticket = create_ticket(
        room=state["room"],
        block=state["block"],
        category=state["category"],
        priority=state["priority"],
        description=state["description"],
        assigned_to=state["assigned_to"],
    )
    return {"ticket": ticket}


def build_graph():
    graph = StateGraph(ComplaintState)
    graph.add_node("extract", extract_node)
    graph.add_node("classify", classify_node)
    graph.add_node("priority", priority_node)
    graph.add_node("assign", assign_node)
    graph.add_node("ticket", ticket_node)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "classify")
    graph.add_edge("classify", "priority")
    graph.add_edge("priority", "assign")
    graph.add_edge("assign", "ticket")
    graph.add_edge("ticket", END)

    return graph.compile()


complaint_agent = build_graph()


def run_complaint_agent(raw_text):
    result = complaint_agent.invoke({"raw_text": raw_text})
    return result["ticket"]
