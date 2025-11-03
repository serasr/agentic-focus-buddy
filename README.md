# Focus Buddy (Agentic v3.2)

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Autonomous_Agent-red)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Focus Buddy** is an **autonomous AI agent** that helps you plan deep-work sessions intelligently.  
It uses **LangGraph** for reasoning, routing, and reflection, and now, with **persistent memory**, it remembers your past sessions to personalize your focus plans.

**Focus Buddy v3.2** adds self-feedback telemetry -> enabling your AI agent to learn from how you actually work, not just what you plan.

It’s no longer guessing your patterns, it’s beginning to observe them.

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
## What’s New (v3.2)

| Feature | Description |
|----------|-------------|
| Structured Memory | Records actual focus duration, fatigue score, and breaks taken. |
| Feedback Buttons | New Gradio UI lets you log feedback after each session. |
| Adaptive Reflection | Uses real averages to personalize pacing. |
| Learning Loop | From semantic guessing → behavioral adaptation. |

---

## Why It Matters

> v3.1 gave Focus Buddy memory.  
> v3.2 gives it awareness.

This bridges the gap between “adaptive prompts” and “learning behavior.”  
It’s the first step toward an agent that truly personalizes itself through your feedback.

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

## Project Structure

```
focus-buddy-agent/
├─ focus_buddy_langgraph.py   # Core agentic logic (LangGraph + RAG + Memory + self-feedback)
├─ focus_buddy_rag.py         # Retrieval pipeline (SerpAPI-based)
├─ focus_buddy.py             # Simple agent
├─ memory_manager.py          # Memory handler  
├─ app.py                     # Gradio web UI
├─ sample_focus_memory.json   # Sample file depicting how memory is stored locally. This file will be created when the app is run.
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

