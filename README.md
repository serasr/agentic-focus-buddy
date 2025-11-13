# 🤖 Focus Buddy v4.0  
### *Context-Aware. Memory-Driven. MCP-Ready.*

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Autonomous_Agent-red)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Focus Buddy** is an **autonomous AI agent** that helps you plan deep-work sessions intelligently.  
It uses **LangGraph** for reasoning, routing, and reflection, and now, with **persistent memory**, it remembers your past sessions to personalize your focus plans.

Focus Buddy v4.0 marks a major leap in my **Agentic AI Learning-in-Public series**.

For the first time, the agent becomes both:

- **World-aware** - it reads your calendar and tasks (via MCP-style context tools)  
- **Self-aware** - it learns from your fatigue, breaks, and focus patterns over time  

This creates a deeply adaptive planning agent that doesn’t just respond, it *understands*, *learns*, and *adjusts*.


---

# Why v4.0 Is Different

Most AI assistants answer questions.

But an **agent** should:

- Observe the world  
- Reason over context  
- Reflect on past behavior  
- Adapt its strategy  
- Take actions (like scheduling your focus block)

Focus Buddy v4.0 now does all of this.

---

# New in v4.0

## 1. MCP-Style Context Integration

Your agent now consults two external sources before planning:

### Calendar MCP Mock  
Finds your *free focus slots* automatically.

### Task MCP Mock  
Looks at your top pending tasks and includes them in the reasoning.

Both mocks are designed with the same interfaces real MCP servers use.  
Swapping them with Google Calendar / Notion / Todoist MCP will require **zero changes to your agent logic**.

---

## 2. World + Self Awareness Combined

Focus Buddy uses:

- **Your goal**
- **Your available duration**
- **Calendar free slots**
- **Pending tasks**
- **Your average focus time**
- **Fatigue trends**
- **Break frequency**

…and merges everything into a *personalized* plan.

---

## 3. Autonomous Scheduling

With a single toggle (`auto_schedule=True`):

- The agent picks your next free slot  
- Adds a calendar event via MCP  
- Returns the scheduled confirmation  

This turns planning into *doing*.

---

## 4. Full Memory System Integration

Stored per-session:

- Focus time  
- Fatigue score  
- Breaks taken  
- Reflections  
- Timestamp  

This historical memory directly influences:

- Block length  
- Break timing  
- Realism adjustments  
- Reflection insights  

---

# High-Level Architecture

```
[User Goal + Duration]
        ↓
[MCP Context Agent]
        ↓
[Classifier → focus / research / motivation]
        ↓
[Router]
   ├── Planner Agent (uses memory + context)
   ├── Research Agent
   └── Motivation Agent
        ↓
[Reflection Agent]
        ↓
[Memory Save]
        ↓
[User Feedback → Memory Update]
```

---


## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/serasr/agentic-focus-buddy.git
cd agentic-focus-buddy
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Activate it:
venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-your-key-here
```

If you’re using Agentic RAG:
```bash
SERPAPI_API_KEY=your-serpapi-key
```

### 5. Run the app
```bash
python app.py
```

Then open:  
```bash
http://127.0.0.1:7860
```

---

## Project Structure

```
focus-buddy-agent/
├─ focus_buddy_langgraph.py   # LangGraph agent (context, memory, reflection)
├─ focus_buddy_rag.py         # Retrieval pipeline (SerpAPI-based)
├─ focus_buddy.py             # Simple agent
├─ memory_manager.py          # Memory handler
├── mcp_client.py             # MCP-style mock servers (calendar + tasks)
├─ app.py                     # Gradio web UI
├─ sample_focus_memory.json   # Sample file depicting how memory is stored locally. This file will be created when the app is run.
├── calendar_data.json        # Calendar mock data
├── tasks_data.json           # Tasks mock data
├─ requirements.txt
├─ .env
├─ end-product/
│   └─ v4/                    # Screenshots or demo outputs
├─ README.md
└─ CHANGELOG.md
```

---

## Tech Stack

- **LangGraph** – workflow and routing
- **OpenAI GPT‑4o-mini** – reasoning & planning
- **Gradio** – UI
- **dotenv** – environment loading
- **Local MCP mocks** – calendar + tasks
- **JSON-based memory system** – behavior tracking

---

## Requirements

See `requirements.txt`

---

## Why “Agentic”?

Most AI apps react to input once and stop.  
Focus Buddy *thinks, routes, retrieves, acts, and reflects* - following the **Reason → Act → Reflect** pattern that defines *agentic systems*.

It’s a small example of how agents can move from *reactive tools* → *autonomous collaborators*.

---


## Author
**Created by:** Sera  
Part of the *Agentic AI Learning-in-Public* series; building reasoning-driven systems that bridge productivity, autonomy, and AI design.

---

