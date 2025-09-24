# Agentic Focus Buddy
## Focus Buddy (Agentic v1) - Reason → Act → Reflect

[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue?logo=openai)](https://platform.openai.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Focus Buddy** is a **primitive agentic AI** that helps you plan focused deep-work sessions intelligently.  
Instead of giving a one-shot response, it *thinks*, *acts*, and *reflects* - running a full **Reason → Act → Reflect** loop before delivering a final plan.

This is part of my **Agentic AI - learning-in-public series**, exploring how small reasoning loops can create systems that feel *autonomous* rather than reactive.

---

## How It Works
```
[User Goal]
   ↓
REASON - think through approach, time allocation & structure  
   ↓
ACT - generate a concrete plan (steps, breaks, motivation)  
   ↓
REFLECT - critique and refine the plan for realism  
   ↓
Final Plan delivered to the user
```
> This minimal loop makes Focus Buddy a **genuinely agentic** system - not just a chat script.

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

### Add your API key
```bash
cp .env.example .env
```
Then open `.env` and add:
```
OPENAI_API_KEY=sk-your-key-here
```

### Run locally (Gradio UI)
```bash
python app.py
```
Open http://127.0.0.1:7860 and enter a task + duration.  
Focus Buddy will reason, act, and reflect before showing your final plan.

---

## Example Output
```
Task: Write a 2-page analysis report | Duration: 2 hours

Reasoning:
Divide work into outline → draft → edit. Include breaks to maintain focus.

Initial Plan:
1. Outline structure (0:00–0:30)  
2. Write draft (0:30–1:20)  
3. Break (1:20–1:30)  
4. Revise & polish (1:30–2:00)

Reflection:
Break comes too late - move earlier for mental reset.  
**Final Plan:**  
1. Outline (0:00–0:25)  
2. Draft (0:25–1:15)  
3. Break (1:15–1:25)  
4. Revise (1:25–2:00)

Motivation: You’re not racing the clock - you’re partnering with focus.
```

---

## Project Structure
```
focus-buddy-agent/
├─ focus_buddy.py     # Core Reason→Act→Reflect agent logic  
├─ app.py             # Gradio interface  
├─ requirements.txt  
├─ .env               # Example .env file  
├─ end-product/       # Contains screenshots/demos/images/links of the end-product/output      
    ├─ v1             
├─ README.md  
└─ CHANGELOG.md  
```

## Tech Stack
- **Python 3.9+**  
- **OpenAI API (gpt-4o-mini / gpt-4o)**  
- **Gradio** for UI  
- **dotenv** for secure key loading  

---

## Why “Agentic”?
Unlike a regular LLM that responds once and stops, Focus Buddy *reasons, plans, and reflects* before answering -  
a core pattern behind modern **agentic systems** like AutoGPT, ReAct, and Reflexion.

---

## License
MIT License - see [LICENSE](LICENSE)

---

## Credits & Author
**Created by:** Sera  
Part of my *“Agentic AI”* learning journey, building small, reasoning-driven systems to explore how AI can move from reactive to proactive behavior.
