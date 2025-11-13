"""
MCP-style client with local mock servers.
- CalendarServerMock: returns free slots; can "add" events
- TaskServerMock: returns top tasks; can "complete" a task
These simulate MCP servers so we can wire LangGraph to real context now,
and swap in real MCP servers later.
"""

from __future__ import annotations
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Local “data layer” (simple JSON files)
CAL_PATH = Path("calendar_data.json")
TASK_PATH = Path("tasks_data.json")

def _load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default
    return default

def _save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


# ------------------ Mock Calendar Server ----------------------
class CalendarServerMock:
    name = "calendar"

    @staticmethod
    def get_free_slots(duration_minutes: int, horizon_hours: int = 8) -> List[Dict[str, str]]:
        """
        Return a few free slots today within `horizon_hours` window.
        Very naive: pretends existing events in CAL_PATH occupy time.
        """
        now = datetime.now().replace(second=0, microsecond=0)
        end = now + timedelta(hours=horizon_hours)
        events = _load_json(CAL_PATH, {"events": []}).get("events", [])

        # Build a simple timeline minute-by-minute “occupied” mask
        occupied = []
        for e in events:
            try:
                s = datetime.fromisoformat(e["start"])
                f = datetime.fromisoformat(e["end"])
                occupied.append((max(s, now), min(f, end)))
            except Exception:
                continue

        # Greedy scan for free windows
        cur = now
        slots = []
        step = timedelta(minutes=5)
        block = timedelta(minutes=duration_minutes)

        while cur + block <= end and len(slots) < 3:  # return up to 3 options
            conflict = False
            for (s, f) in occupied:
                if cur < f and (cur + block) > s:
                    conflict = True
                    cur = max(cur, f)  # jump past conflict
                    break
            if not conflict:
                slots.append({
                    "start": cur.isoformat(timespec="minutes"),
                    "end": (cur + block).isoformat(timespec="minutes")
                })
                cur += timedelta(minutes=duration_minutes // 2 or 1)  # stagger suggestions
        return slots

    @staticmethod
    def add_event(title: str, start_iso: str, end_iso: str) -> Dict[str, Any]:
        data = _load_json(CAL_PATH, {"events": []})
        data["events"].append({"title": title, "start": start_iso, "end": end_iso})
        _save_json(CAL_PATH, data)
        return {"ok": True, "added": {"title": title, "start": start_iso, "end": end_iso}}


# ---------------- Mock Task Server ------------------------
class TaskServerMock:
    name = "tasks"

    @staticmethod
    def list_top_tasks(limit: int = 3) -> List[Dict[str, Any]]:
        tasks = _load_json(TASK_PATH, {"tasks": []}).get("tasks", [])
        # naive priority sort: earlier due date first, then incomplete
        tasks.sort(key=lambda t: (t.get("done", False), t.get("due", "9999-12-31")))
        return tasks[:limit]

    @staticmethod
    def complete_task(task_id: str) -> Dict[str, Any]:
        data = _load_json(TASK_PATH, {"tasks": []})
        found = False
        for t in data["tasks"]:
            if t.get("id") == task_id:
                t["done"] = True
                found = True
                break
        _save_json(TASK_PATH, data)
        return {"ok": found, "id": task_id}


# --------------------------- MCP Client -------------------------
class MCPClient:
    """
    This mimics MCP client behavior.
    In real MCP, this would handle transport, schemas & capability negotiation.
    Here, we just route (server, tool) to local mock servers.
    """
    def __init__(self):
        self._servers = {
            CalendarServerMock.name: CalendarServerMock,
            TaskServerMock.name: TaskServerMock,
        }

    def call(self, server: str, tool: str, args: Optional[Dict[str, Any]] = None) -> Any:
        if server not in self._servers:
            raise ValueError(f"Unknown server: {server}")
        srv = self._servers[server]
        if not hasattr(srv, tool):
            raise ValueError(f"Unknown tool '{tool}' on server '{server}'")
        return getattr(srv, tool)(**(args or {}))
