import json
import os
from datetime import datetime

MEMORY_FILE = "focus_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_memory(entry):
    """Appends structured memory entry to persistent file."""
    data = load_memory()
    data.append(entry)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_session(goal, duration, reflection, actual_focus=None, fatigue_score=None, breaks_taken=0):
    """Stores structured feedback for each session."""
    entry = {
        "goal": goal,
        "duration": duration,
        "reflection": reflection,
        "actual_focus_minutes": actual_focus,
        "breaks_taken": breaks_taken,
        "fatigue_score": fatigue_score,
        "timestamp": datetime.now().isoformat()
    }
    save_memory(entry)


def get_recent_sessions(n=3):
    """Returns recent sessions as text for reflection context."""
    data = load_memory()[-n:]
    if not data:
        return "No previous sessions found."
    summary = []
    for d in data:
        fatigue = f" (fatigue {d['fatigue_score']}/5)" if d.get("fatigue_score") else ""
        summary.append(f"- {d['goal']} ({d['duration']}) → focus {d.get('actual_focus_minutes','?')} min{fatigue}")
    return "\n".join(summary)


def compute_average_focus_time():
    """Computes avg actual focus minutes from recorded memory."""
    data = [d for d in load_memory() if d.get("actual_focus_minutes")]
    if not data:
        return None
    total = sum(d["actual_focus_minutes"] for d in data)
    return round(total / len(data), 1)
