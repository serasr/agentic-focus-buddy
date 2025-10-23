"""
app.py - Gradio Interface for Focus Buddy v3.0
----------------------------------------------
Launch a web UI to run a complete focus session:
User enters a goal + duration → Agent classifies, plans, retrieves (RAG), reflects → returns structured plan.
"""

import gradio as gr
from focus_buddy_langgraph import run_focus_session

def run_agent(goal, duration):
    if not goal or not duration:
        return "Please enter both a goal and duration."
    try:
        result = run_focus_session(goal, duration)
        return result
    except Exception as e:
        return f"Error while running Focus Buddy: {e}"

with gr.Blocks(title="Focus Buddy v3.0 - Agentic Focus Session") as demo:
    gr.Markdown("""
    # Focus Buddy (Agentic v3.0)
    **An autonomous AI assistant that plans, retrieves, and reflects.**

    Give it a goal and time - it’ll reason through the best approach,
    find relevant strategies, create your focus plan, and self-reflect.
    """)

    with gr.Row():
        goal = gr.Textbox(label=" Your Goal", placeholder="Finish a data analysis report")
        duration = gr.Textbox(label=" Duration", placeholder="2 hours")

    run_btn = gr.Button("Generate Focus Plan")

    output = gr.Markdown(label="Focus Buddy Plan", show_copy_button=True)

    run_btn.click(fn=run_agent, inputs=[goal, duration], outputs=output)

    gr.Markdown("---")
    gr.Markdown("Built with using LangGraph, OpenAI, and Gradio.")

if __name__ == "__main__":
    demo.launch()
