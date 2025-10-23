# Focus Buddy (Agentic v3.0)

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Autonomous_Agent-red)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Focus Buddy** is an **autonomous AI agent** that plans your deep-work sessions intelligently.  
Unlike a chatbot, it doesn’t just respond, rather it *thinks, retrieves, and reflects* before presenting a final, personalized focus plan.

This is part of the **Agentic AI: Learning in Public Series**, exploring how reasoning loops, retrieval, and autonomy can make AI systems more *intentional* and *goal-driven*.

---

## Version Highlights (v3.0)

| Capability | Description |
|-------------|--------------|
| **Session-based design** | You give it a goal and duration - it handles everything autonomously. |
| **Agentic autonomy (LangGraph)** | Classifies → Routes → Executes → Reflects using reasoning loops. |
| **Agentic RAG integration** | Retrieves real-world productivity and research insights using SerpAPI. |
| **Self-reflection step** | Evaluates and refines its own plan for realism and flow. |
| **Gradio UI** | Simple web interface to interact with Focus Buddy visually. |

---

## How It Works

```
[User Goal + Duration]
      ↓
CLASSIFY — identify if the task needs planning, research, or motivation  
      ↓
ROUTE — decide which specialized sub-agent to activate  
      ↓
ACT — run planner / research / motivator (with RAG for real context)  
      ↓
REFLECT — review and refine the plan before final output  
      ↓
Return structured focus plan with reasoning + motivation
```

> Focus Buddy isn’t just conversational, it *acts with intent.*

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

**Input**
```
Goal: Finish a literature review on generative AI ethics
Duration: 3 hours
```

**Output**
```
Classifier → research
Routing to: research_agent

Focus Buddy Plan for: Finish a literature review on generative AI ethics
--------------------------------------------------
1. Scan recent AI ethics papers (0:00–0:40)
2. Extract key arguments (0:40–1:20)
3. Draft comparison summary (1:20–2:20)
4. Review and synthesize (2:20–3:00)

Reflection:
The pacing looks good. Add a short 10-min stretch between steps 2 and 3 for cognitive reset.

Motivation:
"Curiosity fuels clarity - let it guide your review."
```

---

## Project Structure

```
focus-buddy-agent/
├─ focus_buddy_langgraph.py   # Core agentic logic (LangGraph + RAG)
├─ focus_buddy_rag.py         # Retrieval pipeline (SerpAPI-based)
├─ focus_buddy.py             # Simple agent 
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

## Author
**Created by:** Sera  
Part of the *Agentic AI Learning-in-Public* series — building reasoning-driven systems that bridge productivity, autonomy, and AI design.

---

