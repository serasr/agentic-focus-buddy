"""
Gradio Interface - Focus Buddy v3.1 (Autonomous + Memory)
----------------------------------------------------------
Now remembers your previous sessions and adapts reflection
based on your working patterns.
"""

import gradio as gr
from focus_buddy_langgraph_updated_memory import run_focus_session
from memory_manager import get_recent_preferences

# -----------------------------------------------
# Helper for showing memory context
# -----------------------------------------------
def show_memory():
    prefs = get_recent_preferences()
    if prefs:
        return f"Recent Focus Sessions:\n{prefs}"
    return "No previous sessions found yet."

# -----------------------------------------------
# Main interaction logic
# -----------------------------------------------
def run_agent(goal, duration):
    if not goal or not duration:
        return "Please enter both a goal and duration.", "", ""
    try:
        result = run_focus_session(goal, duration)
        memory = get_recent_preferences()
        return result, f"Focus Buddy remembers this session!\n\n{memory or ''}", ""
    except Exception as e:
        return f"Error: {e}", "", ""

# -----------------------------------------------
# Gradio App Layout
# -----------------------------------------------
with gr.Blocks(title="Focus Buddy v3.1 — Autonomous + Memory") as demo:
    gr.Markdown("""
# Focus Buddy (Agentic v3.1)
Your AI companion that **plans, reflects, and now remembers** your focus sessions.
Powered by LangGraph + Agentic RAG + Memory.
""")

    with gr.Row():
        goal = gr.Textbox(label="Your Goal", placeholder="e.g. Finish my data analysis report")
        duration = gr.Textbox(label="⏱Duration", placeholder="e.g. 2 hours")

    btn = gr.Button("Generate Focus Plan")

    with gr.Row():
        plan_output = gr.Markdown(label="Final Focus Plan", show_copy_button=True)
        memory_output = gr.Markdown(label="Memory Log", show_copy_button=False)

    btn.click(run_agent, [goal, duration], [plan_output, memory_output])

    gr.Markdown("---")
    gr.Markdown("### Session Memory Overview")
    memory_display = gr.Textbox(
        label="Recent Sessions",
        value=show_memory(),
        lines=6,
        interactive=False,
    )

    gr.Markdown("---")
    gr.Markdown("Built with ❤️ LangGraph · OpenAI · Gradio")

if __name__ == "__main__":
    demo.launch()
