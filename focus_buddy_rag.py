"""
Focus Buddy v2.0 - Manual Agentic RAG
--------------------------------------
This version extends Focus Buddy by adding retrieval-augmented reasoning.
It searches for focus/productivity insights and integrates them into the plan.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPEN_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# Initialize tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=openai_api_key)
search = SerpAPIWrapper(serpapi_api_key= serpapi_api_key)

# Prompt Template 
template = """
You are Focus Buddy - an AI assistant that helps users focus effectively.

Task: {task}
Duration: {duration}

Below is some information gathered from web search to help you plan better:
--------------------
{context}
--------------------

Now:
1. Summarize the most useful focus/productivity strategies from the context.
2. Create a personalized focus plan (include reasoning and timing).
3. Explain briefly why this plan will work.
4. End with a short motivational reflection.

Format output as:

### Strategy Summary
...
### Focus Plan
...
### Why This Works
...
### Motivation
...
"""

prompt = PromptTemplate(
    input_variables=["task", "duration", "context"],
    template=template,
)

# Core Function 
def run_agentic_rag(task: str, duration: str) -> str:
    """
    Runs a simple Retrieval-Augmented Generation (RAG) pipeline.
    1. Searches the web for relevant insights.
    2. Injects context into the LLM.
    3. Generates a structured focus plan.
    """
    try:
        # Step 1 - Retrieve relevant info
        query = f"focus and productivity strategies for {task}"
        context = search.run(query)

        # Step 2 - Reason & generate plan
        final_prompt = prompt.format(task=task, duration=duration, context=context)
        result = llm.invoke(final_prompt)

        return result.content

    except Exception as e:
        return f"Error: {e}"


# Local Test 
#if __name__ == "__main__":
#    print("Running Focus Buddy v2.0 - Manual Agentic RAG\n")
#    task = "Write a 3-page research report"
#    duration = "2 hours"
#    output = run_agentic_rag(task, duration)
#    print(output)
