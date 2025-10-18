import gradio as gr
from focus_buddy_rag import run_agentic_rag  # for v2.0

def run(task, duration):
    if not task or not duration:
        return "Please provide both Task and Duration.", "", ""
    
    # Call the new Agentic RAG function
    output = run_agentic_rag(task, duration)
    
    # Since RAG version returns a single structured response, fill the main box
    return output, "Retrieved and reasoned using web context.", "N/A (RAG does direct reasoning)"

# Gradio UI
with gr.Blocks(title="Focus Buddy (Agentic RAG v2.0)") as demo:
    gr.Markdown("# Focus Buddy (Agentic RAG v2.0)")
    gr.Markdown(
        "An enhanced Focus Buddy powered by **Retrieval-Augmented Reasoning**. "
        "It searches for real productivity insights before planning."
    )

    with gr.Row():
        task = gr.Textbox(label="Your Task", placeholder="Write a 2-page analysis report")
        duration = gr.Textbox(label="Time Available", placeholder="2 hours")

    btn = gr.Button("Generate Focus Plan")
    final_plan = gr.Markdown(label="Final Plan")
    with gr.Accordion("Reasoning (context summary)", open=False):
        reasoning = gr.Textbox(lines=10)
    with gr.Accordion("Initial Plan (pre-reflection)", open=False):
        initial = gr.Textbox(lines=10)

    btn.click(run, [task, duration], [final_plan, reasoning, initial])

# Launch app 
if __name__ == "__main__":
    demo.launch()
