# Agentic Focus Buddy
## Focus Buddy (Agentic v1 → v2) - From Reason → Act → Reflect → Retrieve

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Focus Buddy** is an evolving **Agentic AI assistant** that helps you plan focused deep-work sessions intelligently.  
Version 1 introduced a minimal **Reason → Act → Reflect** loop, while Version 2 expands it into a lightweight form of **Agentic RAG** (Retrieval-Augmented Reasoning).

This project is part of my **Agentic AI: learning-in-public series**, where I iteratively build, deploy, and reflect on systems that feel *autonomous rather than reactive*.

---

## Version 2.0 - Agentic RAG

**What’s new:**
- **Retrieval-Augmented Reasoning** - integrates real web insights using SerpAPI.  
- Uses retrieved context to plan smarter, more realistic focus sessions.  
- Works as a stepping stone toward true autonomous agents (LangGraph in v3).

### How It Works (v2.0)
```
[User Goal]
   ↓
REASON - interpret the goal and duration  
   ↓
RETRIEVE - fetch relevant focus/productivity strategies from the web  
   ↓
ACT - generate a structured plan using retrieved knowledge  
   ↓
REFLECT - explain why this plan works  
   ↓
DELIVER - output a refined, context-aware focus plan
```
> This extends Focus Buddy into a **retrieval-augmented agent**, grounding its reasoning in live information.

---

## Example Output (v2.0)
```
Strategy Summary
- Use 50/10 focus cycles (Pomodoro)
- Minimize distractions using task batching

Focus Plan
1. 0–50 min: Outline report sections
2. 50–60 min: Short break
3. 60–110 min: Write core content
4. 110–120 min: Revise and finalize

Why This Works
Incorporates evidence-based attention management strategies for sustained focus.

Motivation
Every focused cycle compounds - momentum builds with each 50-minute block.
```

---

## Quickstart
### Clone the repo
```bash
git clone https://github.com/serasr/agentic-focus-buddy.git
cd agentic-focus-buddy
```

### Create a virtual environment
```bash
python -m venv .venv  
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Add your API keys
Create a `.env` file:
```
OPENAI_API_KEY=<your-openai-key-here>
SERPAPI_API_KEY=<your-serpapi-key-here>
```

### Run locally (Gradio UI)
```bash
python app.py
```
Open [http://127.0.0.1:7860](http://127.0.0.1:7860)  
Enter a task & duration, and Focus Buddy will retrieve insights, reason, and generate your plan.

---

## Version History

### v2.0 - Agentic RAG
- Introduced web retrieval via SerpAPI  
- Combined external context + reasoning for smarter plans  
- Updated Gradio UI for unified output

### v1.0 - Reason → Act → Reflect
- Primitive reasoning loop with interpret → plan → refine  
- No external context  
- Core logic in `focus_buddy.py`

---

## Project Structure
```
focus-buddy-agent/
├─ focus_buddy.py          # v1.0 Reason → Act → Reflect agent logic  
├─ focus_buddy_rag.py      # v2.0 Manual Agentic RAG  
├─ app.py                  # Gradio UI (integrated with RAG backend)  
├─ requirements.txt  
├─ .env.example  
├─ README.md  
└─ CHANGELOG.md  
```

---

## Tech Stack
- **Python 3.9+**  
- **LangChain 1.0+**  
- **OpenAI GPT-4o-mini**  
- **SerpAPI** for live retrieval  
- **Gradio** for UI  
- **dotenv** for secure key management  

---

## Why “Agentic”?
Unlike traditional LLMs that just respond once, Focus Buddy *reasons, retrieves, and reflects* -  
following the core design pattern behind modern **agentic systems** like ReAct, Reflexion, and AutoGPT.

---

## License
MIT License - see [LICENSE](LICENSE)

---

## Credits & Author
**Created by:** Sera 

Part of my *“Agentic AI”* learning journey - building small reasoning-driven systems to explore how AI can move from reactive to proactive behavior.
