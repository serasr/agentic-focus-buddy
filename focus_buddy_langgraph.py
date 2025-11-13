"""
Focus Buddy v4.0 : MCP-ready, Context-Aware Focus Agent
- Uses MCP-style client to fetch:
  - calendar free slots
  - top tasks
- Uses structured memory (from v3.1) for personalization
- Optional auto-scheduling of a focus block into the calendar mock
"""

import os
from typing import Annotated, Literal, Dict, Any

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from memory_manager import (
    record_session,
    compute_average_focus_time,
    get_recent_sessions,
)
from mcp_client import MCPClient

# --- Setup ---
load_dotenv()
openai_api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=openai_api_key)

mcp = MCPClient()


# ---------------------- Helpers --------------------
def parse_duration_to_minutes(text: str) -> int:
    """
    Very small parser: '2 hours' -> 120, '90 min' -> 90, '1.5h' -> 90.
    Defaults to 60 if unclear.
    """
    t = (text or "").lower().strip()
    try:
        if any(k in t for k in ["hour", "hr", "h "]):
            # extract first number-ish token
            num_str = "".join(ch if (ch.isdigit() or ch in ". ") else " " for ch in t)
            toks = [p for p in num_str.split() if p]
            if toks:
                return int(round(float(toks[0]) * 60))
        if "min" in t or "m " in t or t.endswith("m"):
            num_str = "".join(ch if (ch.isdigit() or ch in ". ") else " " for ch in t)
            toks = [p for p in num_str.split() if p]
            if toks:
                return int(round(float(toks[0])))
    except Exception:
        pass
    return 60


def summarize_context(context: Dict[str, Any]) -> str:
    slots = context.get("free_slots", []) or []
    tasks = context.get("top_tasks", []) or []

    if slots:
        slot_lines = [f"- {s['start']} → {s['end']}" for s in slots]
    else:
        slot_lines = ["(no free slots found)"]

    if tasks:
        task_lines = [
            f"- [{t.get('id','?')}] {t.get('title','(untitled)')} "
            f"(due {t.get('due','—')}){' ✅' if t.get('done') else ''}"
            for t in tasks
        ]
    else:
        task_lines = ["(no tasks found)"]

    return "Free slots:\n" + "\n".join(slot_lines) + "\n\nTop tasks:\n" + "\n".join(task_lines)


# ---------------------- State & Classifier ----------------------
class TaskClassifier(BaseModel):
    task_type: Literal["focus", "research", "motivation"] = Field(...)


class State(TypedDict):
    goal: str
    duration: str
    messages: Annotated[list, add_messages]
    task_type: str | None
    context: Dict[str, Any]
    auto_schedule: bool


# ---------------------- Nodes ----------------------
def context_agent(state: State):
    """Fetch external context (calendar slots + top tasks) via MCP client."""
    duration_min = parse_duration_to_minutes(state["duration"])
    free_slots = mcp.call("calendar", "get_free_slots", {"duration_minutes": duration_min})
    top_tasks = mcp.call("tasks", "list_top_tasks", {"limit": 3})
    return {
        "context": {
            "duration_min": duration_min,
            "free_slots": free_slots,
            "top_tasks": top_tasks,
        }
    }


def classify_task(state: State):
    cls = llm.with_structured_output(TaskClassifier)
    res = cls.invoke(
        [
            {
                "role": "system",
                "content": "Classify the goal as 'focus', 'research', or 'motivation'.",
            },
            {"role": "user", "content": state["goal"]},
        ]
    )
    return {"task_type": res.task_type}


def router(state: State):
    t = state.get("task_type", "focus")
    if t == "research":
        return {"next": "research_agent"}
    if t == "motivation":
        return {"next": "motivator_agent"}
    return {"next": "planner_agent"}


def planner_agent(state: State):
    goal = state["goal"]
    duration = state["duration"]
    context = state.get("context", {})
    avg_focus = compute_average_focus_time()
    avg_msg = (
        f"User’s average focus window: ~{avg_focus} minutes."
        if avg_focus is not None
        else "No historical focus data yet."
    )
    ctx_summary = summarize_context(context)

    messages = [
        {
            "role": "system",
            "content": (
                "You are Focus Buddy. Create a realistic, time-bounded plan "
                "using both user history and context (calendar slots + tasks)."
            ),
        },
        {
            "role": "assistant",
            "content": f"{avg_msg}\n\nContext:\n{ctx_summary}",
        },
        {
            "role": "user",
            "content": (
                f"Goal: {goal}\n"
                f"Duration: {duration}\n"
                "Use one of the free slots if possible. Break the work into steps with times."
            ),
        },
    ]

    reply = llm.invoke(messages)
    plan_text = reply.content if hasattr(reply, "content") else str(reply)

    scheduled_info = None
    if state.get("auto_schedule") and context.get("free_slots"):
        first = context["free_slots"][0]
        scheduled_info = mcp.call(
            "calendar",
            "add_event",
            {
                "title": f"Focus: {goal}",
                "start_iso": first["start"],
                "end_iso": first["end"],
            },
        )
        if scheduled_info.get("ok"):
            added = scheduled_info["added"]
            plan_text += (
                f"\n\n📅 Scheduled focus block: {added['start']} → {added['end']}"
            )

    # record a basic session entry (user feedback can add richer data later)
    record_session(
        goal=goal,
        duration=duration,
        reflection="Initial plan (pre-reflection)",
        actual_focus=None,
        fatigue_score=None,
        breaks_taken=0,
    )

    return {"messages": [{"role": "assistant", "content": plan_text}]}


def research_agent(state: State):
    goal = state["goal"]
    ctx_summary = summarize_context(state.get("context", {}))
    reply = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You are a research-focused assistant. Use the given context only "
                    "as background; propose concise research strategies."
                ),
            },
            {"role": "assistant", "content": f"Context:\n{ctx_summary}"},
            {"role": "user", "content": goal},
        ]
    )
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def motivator_agent(state: State):
    goal = state["goal"]
    reply = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You are a motivational coach. Encourage the user and give a short, "
                    "grounding affirmation tied to their goal."
                ),
            },
            {"role": "user", "content": goal},
        ]
    )
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def reflection_agent(state: State):
    last = state["messages"][-1]
    text = last.content if hasattr(last, "content") else str(last)
    recent = get_recent_sessions()
    ctx_summary = summarize_context(state.get("context", {}))

    messages = [
        {
            "role": "system",
            "content": (
                "You are the Reflector. Improve the plan using:\n"
                "- pacing and realism\n"
                "- user’s past focus patterns\n"
                "- current context (calendar + tasks)\n"
                "Keep edits small but meaningful."
            ),
        },
        {"role": "assistant", "content": text},
        {
            "role": "user",
            "content": f"Recent sessions:\n{recent}\n\nContext recap:\n{ctx_summary}",
        },
    ]
    reflection = llm.invoke(messages)
    reflection_text = reflection.content if hasattr(reflection, "content") else str(reflection)

    # store reflection as another memory entry
    record_session(
        goal=state["goal"],
        duration=state["duration"],
        reflection=reflection_text,
        actual_focus=None,
        fatigue_score=None,
        breaks_taken=0,
    )

    return {"messages": [{"role": "assistant", "content": reflection_text}]}


# ------------------ Build Graph ----------------------
graph_builder = StateGraph(State)
graph_builder.add_node("context_agent", context_agent)
graph_builder.add_node("classifier", classify_task)
graph_builder.add_node("router", router)
graph_builder.add_node("planner_agent", planner_agent)
graph_builder.add_node("research_agent", research_agent)
graph_builder.add_node("motivator_agent", motivator_agent)
graph_builder.add_node("reflection_agent", reflection_agent)

graph_builder.add_edge(START, "context_agent")
graph_builder.add_edge("context_agent", "classifier")
graph_builder.add_edge("classifier", "router")

graph_builder.add_conditional_edges(
    "router",
    lambda st: st.get("next"),
    {
        "planner_agent": "planner_agent",
        "research_agent": "research_agent",
        "motivator_agent": "motivator_agent",
    },
)

graph_builder.add_edge("planner_agent", "reflection_agent")
graph_builder.add_edge("research_agent", "reflection_agent")
graph_builder.add_edge("motivator_agent", "reflection_agent")
graph_builder.add_edge("reflection_agent", END)

graph = graph_builder.compile()


# --------------- Public Runner ----------------------
def run_focus_session_v4(goal: str, duration: str = "2 hours", auto_schedule: bool = False) -> str:
    state: State = {
        "goal": goal,
        "duration": duration,
        "messages": [],
        "task_type": None,
        "context": {},
        "auto_schedule": auto_schedule,
    }
    final_state = graph.invoke(state)
    last = final_state["messages"][-1]
    return last.content if hasattr(last, "content") else str(last)
