"""
Focus Buddy v3.1 - Autonomous Focus Session Agent
--------------------------------------------------
Uses LangGraph for classification, routing & decision logic
Integrates Agentic RAG (SerpAPI-based) for research tasks
Returns a structured focus plan with reasoning & motivation
"""

# Imports 
import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAIs
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from focus_buddy_rag import run_agentic_rag # from v2.0 focus buddy
from IPython.display import Image, display
from memory_manager import remember_session, get_recent_preferences

# --- Setup ---
load_dotenv()
openai_api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=openai_api_key)
# ----------------------------------------------------
# CLASSIFICATION SCHEMA + STATE
# ----------------------------------------------------
class TaskClassifier(BaseModel):
    task_type: Literal["focus", "research", "motivation"] = Field(
        ...,
        description="Classify the goal as 'focus', 'research', or 'motivation'."
    )

class State(TypedDict):
    goal: str
    duration: str
    messages: Annotated[list, add_messages]
    task_type: str | None


# ----------------------------------------------------
# CLASSIFIER NODE
# ----------------------------------------------------
def classify_task(state: State):
    """Classify the goal type to route to appropriate sub-agent."""
    goal = state["goal"]
    classifier = llm.with_structured_output(TaskClassifier)

    result = classifier.invoke([
        {
            "role": "system",
            "content": """You are Focus Buddy's classifier.
            Determine whether the user's goal is:
            - 'focus' → planning or task execution
            - 'research' → learning or information gathering
            - 'motivation' → emotional uplift or self-discipline"""
        },
        {"role": "user", "content": goal}
    ])

    print(f"Classifier → {result.task_type}")
    return {"task_type": result.task_type}


# ----------------------------------------------------
# ROUTER NODE
# ----------------------------------------------------
def router(state: State):
    """Route based on classification result."""
    task_type = state.get("task_type", "focus")
    print(f"Routing to: {task_type}_agent")

    if task_type == "research":
        return {"next": "research_agent"}
    elif task_type == "motivation":
        return {"next": "motivator_agent"}
    else:
        return {"next": "planner_agent"}


# ----------------------------------------------------
# SUB-AGENTS
# ----------------------------------------------------
def planner_agent(state: State):
    """Create a detailed focus plan for the goal."""
    goal = state["goal"]
    duration = state["duration"]

    messages = [
        {"role": "system", "content": """You are Focus Buddy, an AI planning assistant.
        Your job is to help users execute tasks effectively.
        Create a structured, time-bound plan for focused deep work.
        Include: 
        - Step-by-step breakdown
        - Time allocation
        - Short reasoning
        - 1-line motivational summary."""},
        {"role": "user", "content": f"Goal: {goal}\nDuration: {duration}"}
    ]

    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def research_agent(state: State):
    """Retrieve & summarize context-specific strategies."""
    goal = state["goal"]
    duration = state["duration"]

    print("Running Agentic RAG for research insights...")
    try:
        rag_output = run_agentic_rag(goal, duration)
        return {"messages": [{"role": "assistant", "content": rag_output}]}
    except Exception as e:
        return {"messages": [{"role": "assistant", "content": f"Retrieval failed: {e}"}]}


def motivator_agent(state: State):
    """Provide emotional encouragement and focus mindset."""
    goal = state["goal"]

    messages = [
        {"role": "system", "content": """You are a motivational coach.
        Give emotional support, confidence, and a mindset shift
        tailored to the user's goal. End with a short affirmation."""},
        {"role": "user", "content": goal}
    ]

    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


# ----------------------------------------------------
# REFLECTION NODE
# ----------------------------------------------------
def reflection_agent(state: State):
    """Reflect and refine the plan for realism and flow."""
    last_message = state["messages"][-1]  # AIMessage object

    # Use .content instead of ["content"]
    messages = [
        {"role": "system", "content": """You are the Reflector.
        Review the focus plan for realism, pacing, and clarity.
        Suggest small improvements if necessary."""},
        {"role": "assistant", "content": last_message.content},
    ]

    reflection = llm.invoke(messages)

    refined = f"{last_message.content}\n\n Reflection:\n{reflection.content}"
    return {"messages": [{"role": "assistant", "content": refined}]}



# ----------------------------------------------------
# BUILD THE GRAPH
# ----------------------------------------------------
graph_builder = StateGraph(State)

# Nodes
graph_builder.add_node("classifier", classify_task)
graph_builder.add_node("router", router)
graph_builder.add_node("planner_agent", planner_agent)
graph_builder.add_node("research_agent", research_agent)
graph_builder.add_node("motivator_agent", motivator_agent)
graph_builder.add_node("reflection_agent", reflection_agent)

# Edges
graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {
        "planner_agent": "planner_agent",
        "research_agent": "research_agent",
        "motivator_agent": "motivator_agent"
    }
)

# Reflection step for all
graph_builder.add_edge("planner_agent", "reflection_agent")
graph_builder.add_edge("research_agent", "reflection_agent")
graph_builder.add_edge("motivator_agent", "reflection_agent")
graph_builder.add_edge("reflection_agent", END)

# Compile
graph = graph_builder.compile()

# ----------------------------------------------------
# RUNNING A FOCUS SESSION
# ----------------------------------------------------
def run_focus_session(goal: str, duration: str = "2 hours"):
    """
    Runs a full autonomous focus session:
    Goal → Classify → Route → Execute → Reflect → Save to memory → Return structured output.
    """
    print("Focus Buddy v3.1 -> Agentic Focus Session with Memory\n")

    recent = get_recent_preferences()
    if recent:
        print("Previous Sessions:\n" + recent + "\n")

    state = {
        "goal": goal,
        "duration": duration,
        "messages": [],
        "task_type": None
    }

    final_state = graph.invoke(state)
    last_message = final_state["messages"][-1]
    result = last_message.content if hasattr(last_message, "content") else last_message["content"]

    print(f"\nFocus Buddy Plan for: {goal}\n{'-'*50}\n{result}\n")

    remember_session(goal, duration, result)
    print("Memory Updated! Focus Buddy remembers this session!\n")

    return result


# ----------------------------------------------------
# VISUALIZE LANGGRAPH STRUCTURE (OPTIONAL) & RUNS
# ----------------------------------------------------
if __name__ == "__main__":
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception as e:
        print("Visualization skipped (missing dependencies):", e)

    # Example runs
    run_focus_session("Finish a data analysis report", "2 hours")
    # run_focus_session("Learn how to improve deep work productivity", "1.5 hours")
    # run_focus_session("Get motivated to start my thesis writing", "30 minutes")
