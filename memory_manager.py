# memory_manager.py
import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("focus_memory.json")

def load_memory():
    # Load previous sessions from memory file
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []

def save_memory(memory_data):
    # Save sessions back to file
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory_data, indent=2, ensure_ascii=False), encoding="utf-8")

def remember_session(goal: str, duration: str, plan: str):
    # Add new session entry
    memory = load_memory()
    memory.append({
        "timestamp": datetime.now().isoformat(timespec="minutes"),
        "goal": goal,
        "duration": duration,
        "plan_summary": plan.strip()[:500]
    })
    save_memory(memory)

def get_recent_preferences(limit: int = 3) -> str | None:
    #Return a summary of recent sessions
    memory = load_memory()
    if not memory:
        return None
    recent = memory[-limit:]
    lines = [f"- {m['goal']} ({m['duration']}) @ {m['timestamp']}" for m in recent]
    return "\n".join(lines)
