# Focus Buddy (Agentic v3.1)

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Autonomous_Agent-red)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Focus Buddy** is an **autonomous AI agent** that helps you plan deep-work sessions intelligently.  
It uses **LangGraph** for reasoning, routing, and reflection, and now, with **persistent memory**, it remembers your past sessions to personalize your focus plans.

This version (v3.1) introduces a major leap: Focus Buddy doesn’t just *act* autonomously -> it now *learns and adapts* over time.

---

## Version Highlights (v3.1)

| Capability | Description |
|-------------|--------------|
| **Persistent Memory** | Stores and recalls your past focus sessions for personalized reflection. |
| **Autonomous LangGraph Flow** | Classifies → Routes → Executes → Reflects - no manual control needed. |
| **Agentic RAG** | Integrates SerpAPI-based retrieval for contextual productivity insights. |
| **Gradio Interface** | Intuitive UI with memory log and recent session viewer. |
| **Self-Reflection Loop** | Evaluates and refines its own plan for pacing and realism. |

---

## How It Works

```
[Your Goal + Duration]
      ↓
Classify → Identify goal type (focus / research / motivation)
      ↓
Route → Pick the right sub-agent
      ↓
Act → Generate plan or retrieve insights (Agentic RAG)
      ↓
Reflect → Refine plan based on recent memory + pacing
      ↓
Save → Remember this session for future adaptation
```

> Memory lets Focus Buddy understand *you* over time.

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

## Example Usage

**Input:**
```
Goal: Finish a data analysis report
Duration: 2 hours
```

**Output:**
```
Focus Buddy Plan
--------------------------------------------------
1. Outline analysis structure (0:00–0:25)
2. Draft main findings (0:25–1:15)
3. Take a 10-min mental reset
4. Polish and finalize (1:25–2:00)

Reflection:
Based on your last few sessions, you tend to slow down after 90 minutes.
Added a short break for cognitive refresh.
```

**Memory Saved!**
```
Previous Sessions:
- Write report summary (2 hours) @ 2025-10-25
- Learn LangGraph basics (1.5 hours) @ 2025-10-26
```

---

## Project Structure

```
focus-buddy-agent/
├─ focus_buddy_langgraph.py   # Core agentic logic (LangGraph + RAG + Memory)
├─ focus_buddy_rag.py         # Retrieval pipeline (SerpAPI-based)
├─ focus_buddy.py             # Simple agent
├─ memory_manager.py          # Memory handler  
├─ app.py                     # Gradio web UI
├─ requirements.txt
├─ .env
├─ end-product/
│   └─ v3/                    # Screenshots or demo outputs
├─ README.md
└─ CHANGELOG.md
```

---

## Tech Stack

| Component | Purpose |
|------------|----------|
| **LangGraph** | Autonomous reasoning & control flow |
| **LangChain + OpenAI** | LLM orchestration & structured output |
| **Gradio** | Web interface |
| **SerpAPI** | Real-world retrieval (for RAG) |
| **Pydantic** | Structured classification schemas |
| **dotenv** | Secure API key handling |

---

## Requirements

See `requirements.txt`

---

## Why “Agentic”?

Most AI apps react to input once and stop.  
Focus Buddy *thinks, routes, retrieves, acts, and reflects* - following the **Reason → Act → Reflect** pattern that defines *agentic systems*.

It’s a small example of how agents can move from *reactive tools* → *autonomous collaborators*.

---

## Conceptual Insight

> **RAG helps agents answer with knowledge.**  
> **Memory helps them act with continuity.**
 
RAG enriches responses. Memory builds *identity.*


## Author
**Created by:** Sera  
Part of the *Agentic AI Learning-in-Public* series; building reasoning-driven systems that bridge productivity, autonomy, and AI design.

---

