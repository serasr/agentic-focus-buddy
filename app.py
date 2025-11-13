import gradio as gr
from focus_buddy_langgraph import run_focus_session_v4
from memory_manager import get_recent_sessions, record_session


def run_agent(goal, duration, auto_schedule):
    if not goal or not duration:
        return "⚠️ Please enter both goal and duration.", "No previous sessions yet."
    plan = run_focus_session_v4(goal, duration, auto_schedule=auto_schedule)
    recent = get_recent_sessions()
    return plan, recent


def submit_feedback(goal, duration, fatigue, breaks, focus_time):
    if not goal or not duration:
        return "⚠️ Please enter the same goal + duration you just worked on."
    try:
        focus_int = int(focus_time) if focus_time is not None else None
    except ValueError:
        focus_int = None

    record_session(
        goal=goal,
        duration=duration,
        reflection="User feedback after execution.",
        actual_focus=focus_int,
        fatigue_score=int(fatigue) if fatigue is not None else None,
        breaks_taken=int(breaks) if breaks is not None else 0,
    )
    return "Feedback saved! Future plans will adapt to this pattern."


with gr.Blocks(title="Focus Buddy v4.0 — MCP-ready & Self-aware") as demo:
    gr.Markdown(
        "# 🤖 Focus Buddy v4.0\n"
        "Context-aware, memory-driven focus planning.\n"
        "Uses mock MCP servers (calendar + tasks) + your feedback to adapt."
    )

    with gr.Row():
        goal = gr.Textbox(label="Your Goal", placeholder="Finish my data analysis report")
        duration = gr.Textbox(label="Duration", placeholder="2 hours")

    auto_schedule = gr.Checkbox(
        label="Auto-schedule first free slot to calendar",
        value=False,
    )

    run_btn = gr.Button("Generate Plan")

    plan_out = gr.Markdown(label="Plan / Reflection", show_copy_button=True)
    memory_out = gr.Textbox(label="Recent Sessions", lines=8)

    run_btn.click(run_agent, [goal, duration, auto_schedule], [plan_out, memory_out])

    gr.Markdown("## Log Your Session Feedback")
    fatigue = gr.Slider(1, 5, step=1, label="Fatigue (1 = fresh, 5 = exhausted)", value=3)
    breaks = gr.Number(label="Breaks Taken", value=0)
    focus_time = gr.Number(label="Actual Focus Time (minutes)", value=0)

    submit_btn = gr.Button("Save Feedback 💾")
    status = gr.Textbox(label="Status", lines=2)

    submit_btn.click(
        submit_feedback,
        [goal, duration, fatigue, breaks, focus_time],
        [status],
    )

if __name__ == "__main__":
    demo.launch()
