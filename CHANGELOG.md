# Changelog

All notable changes to this project will be documented in this file.

---

## [v4.0] - 2025-11-13
### Added
- Added `mcp_client.py`  
- Introduced CalendarServerMock  
- Introduced TaskServerMock  
- Synchronous `mcp.call(server, tool, args)` interface  
- Enables future replacement with real MCP servers (Google Calendar, Notion)

---

## [v3.2] - 2025-11-01
### Added
- Self-feedback telemetry in Gradio interface (fatigue slider, breaks, focus time).
- Structured memory system with numeric fields.
- Adaptive reflection using computed average focus duration.
- Planner adapts based on recorded historical focus data.

### Fixed
- Occasional JSON decode errors on corrupted `focus_memory.json`.
- Minor prompt alignment inconsistencies.

---

## [v3.1] - 2025-10-30
### Added
- Introduced **persistent memory** (`memory_manager.py`) to store recent focus sessions.
- Reflection agent now accesses memory context to adapt pacing and structure.
- Updated **Gradio UI** to display recent sessions and memory log in real time.
- Added visualization of recent sessions before each new run.
- Extended reflection node prompt to incorporate personalized context.

### Improved
- Refined system messages for planner, motivator, and reflector for consistency.
- Enhanced readability of generated plans with clearer section breaks.
- Improved classification robustness using structured output (Pydantic schema).

---
## [v3.0] - 2025-10-23
### Added
- Migrated from rule-based loops to **LangGraph** autonomous flow.
- Added multiple sub-agents: `planner_agent`, `research_agent`, `motivator_agent`.
- Integrated structured output classification via `TaskClassifier` using Pydantic.
- Added routing logic for task-type-based agent activation.

### Improved
- Enhanced reasoning flow for “Reason → Act → Reflect”.
- Introduced modular design for adding more tools (retrieval, reflection, scheduling).

---

## [v2.0] - 2025-10-14
### Added
- Introduced **Agentic RAG** (Retrieval-Augmented Reasoning) using SerpAPI.
- Integrated **web-based retrieval** for dynamic productivity strategies.
- Updated Gradio interface to support unified structured output.
- Added `.env` for easier key configuration.
- Enhanced documentation and README for v2.0 transition.

### Changed
- `app.py` now connects to `focus_buddy_rag.py` instead of the primitive loop.
- Switched from static reasoning to context-driven planning.

### Notes
- v2.0 sets the foundation for **v3.0 (LangGraph Autonomous Agent)** — coming next.

---

## [v1.0] - 2025-09-24
### Added
- Initial release of **Focus Buddy (Agentic v1)**.
- Implemented primitive **Reason → Act → Reflect** agent loop.
- Added Gradio-based UI for generating structured focus plans.
- Introduced MIT License and basic project scaffolding.
