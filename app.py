import gradio as gr
from focus_buddy import focus_buddy_agent

def run(task, duration):
    if not task or not duration:
        return "Please provide both Task and Duration.", "", ""
    out = focus_buddy_agent(task, duration)
    return out["final_plan"], out["reasoning"], out["initial_plan"]

with gr.Blocks(title="Focus Buddy (Agentic v1)") as demo:
    gr.Markdown("Focus Buddy (Agentic v1)")
    gr.Markdown("Primitive agentic loop: **Reason → Act → Reflect**.")

    with gr.Row():
        task = gr.Textbox(label="Your Task", placeholder="Write a 2-page analysis report")
        duration = gr.Textbox(label="Time Available", placeholder="2 hours")

    btn = gr.Button("Generate Focus Plan")
    final_plan = gr.Textbox(label="Final Plan", lines=12)
    with gr.Accordion("Reasoning (internal)", open=False):
        reasoning = gr.Textbox(lines=10)
    with gr.Accordion("Initial Plan (pre-reflection)", open=False):
        initial = gr.Textbox(lines=10)

    btn.click(run, [task, duration], [final_plan, reasoning, initial])

demo.launch()
