from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=api_key)

def reason(task,duration):
    prompt = f""" 
    You are a focus buddy, an Agentic AI helping users plan focused work sessions.

    Task = {task}
    Duration = {duration}

    Step 1: Think through this problem.
    -> How should time be divided?
    -> What’s the ideal work-to-break ratio?
    -> What’s the right flow of focus tasks?

    Write your reasoning clearly and concisely.
    """

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role":"system", "content":"You are a reasoning assisstant"},
                  {"role":"user","content":prompt}]
    )

    reasoning = response.choices[0].message.content

    return reasoning


def act(reasoning, task, duration):
    prompt = f"""
    Using this reasoning:
    {reasoning}

    Create a clear, structured focus plan for:
    - Task: {task}
    - Duration: {duration}

    Include:
    1. Step-by-step timeline
    2. Breaks
    3. One motivational line at the end
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"assistant","content":"reasoning"},
                  {"role":"user","content":prompt}]
    )

    plan = response.choices[0].message.content

    return plan

def reflect(plan, duration):
    prompt=f"""
    Here is your initial plan:
    {plan}

    Review it critically:
    - Is it realistic for {duration}?
    - Are breaks reasonable?
    - Can any step be improved?

    Give me the REVISED FINAL PLAN.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"assistant","content":plan},
                  {"role":"user","content":prompt}]
    )

    reflection = response.choices[0].message.content

    return reflection

def focus_buddy_agent(task,duration):
    reasoning = reason(task, duration)
    initial_plan = act(reasoning, task, duration)
    final_plan = reflect(initial_plan, duration)

    return {
        "reasoning": reasoning,
        "initial_plan": initial_plan,
        "final_plan": final_plan
    }


focus_buddy_agent("Write a 2-page analysis report", "2 hours")


