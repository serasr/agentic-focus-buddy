"""
Focus Buddy v3.2 - Understanding your focus patterns
----------------------------------------------------
"""

# --- Imports ---
import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from memory_manager import record_session, get_recent_sessions, compute_average_focus_time

# --- Setup ---
load_dotenv()
openai_api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=openai_api_key)

# --- State schema ---
class TaskClassifier(BaseModel):
    task_type: Literal["focus", "research", "motivation"] = Field(...)

class State(TypedDict):
    goal: str
    duration: str
    messages: Annotated[list, add_messages]
    task_type: str | None


# --- Classifier Node ---
def classify_task(state: State):
    goal = state["goal"]
    classifier = llm.with_structured_output(TaskClassifier)
    result = classifier.invoke([
        {"role": "system", "content": "Classify the goal as focus, research, or motivation."},
        {"role": "user", "content": goal}
    ])
    return {"task_type": result.task_type}


# --- Router Node ---
def router(state: State):
    t = state.get("task_type", "focus")
    return {"next": f"{t}_agent"}


# --- Agents ---
def planner_agent(state: State):
    goal, duration = state["goal"], state["duration"]
    avg_focus = compute_average_focus_time()
    avg_msg = f"Your average focus time is around {avg_focus} minutes." if avg_focus else "No focus history yet."
    msgs = [
        {"role": "system", "content": "You are Focus Buddy. Create structured focus plans with time blocks."},
        {"role": "assistant", "content": avg_msg},
        {"role": "user", "content": f"Goal: {goal}\nDuration: {duration}"}
    ]
    reply = llm.invoke(msgs)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def research_agent(state: State):
    goal = state["goal"]
    reply = llm.invoke([
        {"role": "system", "content": "Provide quick contextual research strategies for the task."},
        {"role": "user", "content": goal}
    ])
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def motivator_agent(state: State):
    goal = state["goal"]
    reply = llm.invoke([
        {"role": "system", "content": "Motivate the user with encouragement and perspective."},
        {"role": "user", "content": goal}
    ])
    return {"messages": [{"role": "assistant", "content": reply.content}]}


# --- Reflection Agent ---
def reflection_agent(state: State):
    last_message = state["messages"][-1]
    recent = get_recent_sessions()
    avg_focus = compute_average_focus_time()
    msg = [
        {"role": "system", "content": "You are a reflective planner. Adjust pacing and structure using user history."},
        {"role": "assistant", "content": last_message.content},
        {"role": "user", "content": f"Past sessions:\n{recent}\nAverage focus time: {avg_focus or 'N/A'} minutes"}
    ]
    reflection = llm.invoke(msg)
    record_session(state["goal"], state["duration"], reflection.content)
    return {"messages": [{"role": "assistant", "content": reflection.content}]}


# --- Build Graph ---
graph = StateGraph(State)

# --- Add nodes ---
graph.add_node("classifier", classify_task)
graph.add_node("router", router)
graph.add_node("planner_agent", planner_agent)
graph.add_node("research_agent", research_agent)
graph.add_node("motivator_agent", motivator_agent)
graph.add_node("reflection_agent", reflection_agent)

# --- Add edges ---
graph.add_edge(START, "classifier")
graph.add_edge("classifier", "router")
graph.add_conditional_edges(
    "router",
    lambda s: s.get("next"),
    {
        "focus_agent": "planner_agent",
        "research_agent": "research_agent",
        "motivation_agent": "motivator_agent"
    },
)
graph.add_edge("planner_agent", "reflection_agent")
graph.add_edge("research_agent", "reflection_agent")
graph.add_edge("motivator_agent", "reflection_agent")
graph.add_edge("reflection_agent", END)

graph = graph.compile()


# --- Run focus sessions ---
def run_focus_session(goal, duration):
    state = {"goal": goal, "duration": duration, "messages": [], "task_type": None}
    final_state = graph.invoke(state)
    msg = final_state["messages"][-1].content
    return msg
