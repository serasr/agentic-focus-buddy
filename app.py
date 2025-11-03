"""
Gradio Interface - Focus Buddy v3.2 
----------------------------------------------------------
Now remembers your previous sessions and adapts reflection
based on your working patterns and your feedback.
"""

import gradio as gr
from focus_buddy_langgraph import run_focus_session
from memory_manager import record_session, get_recent_sessions

# Run Focus Session
def run_agent(goal, duration):
    if not goal or not duration:
        return "Please enter both goal and duration.", ""
    plan = run_focus_session(goal, duration)
    return plan, get_recent_sessions()

# Capture feedback
def submit_feedback(goal, duration, fatigue, breaks, focus_time):
    record_session(goal, duration, reflection="User feedback",
                   actual_focus=focus_time, fatigue_score=fatigue, breaks_taken=breaks)
    return f"Feedback saved! Fatigue={fatigue}, Focus={focus_time}min, Breaks={breaks}"

with gr.Blocks(title="Focus Buddy v3.2 - Self-Feedback AI") as demo:
    gr.Markdown("# Focus Buddy v3.2\nNow learning from how *you* work.")
    with gr.Row():
        goal = gr.Textbox(label="Task", placeholder="e.g. Finish analysis report")
        duration = gr.Textbox(label="Duration", placeholder="e.g. 2 hours")
    run_btn = gr.Button("Generate Plan")
    plan_out = gr.Markdown(label="Focus Plan")
    memory = gr.Textbox(label="Recent Sessions", lines=2)
    run_btn.click(run_agent, [goal, duration], [plan_out, memory])

    gr.Markdown("### Log Your Session Feedback")
    fatigue = gr.Slider(1, 5, label="Fatigue Level (1=Fresh, 5=Tired)")
    breaks = gr.Number(label="Breaks Taken", value=0)
    focus_time = gr.Number(label="Actual Focus Time (minutes)", value=0)
    submit_btn = gr.Button("Save Feedback 💾")
    status = gr.Textbox(label="Status", lines=2)
    submit_btn.click(submit_feedback, [goal, duration, fatigue, breaks, focus_time], [status])

if __name__ == "__main__":
    demo.launch()

