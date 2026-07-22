"""Integrate the agents using LangGraph."""

from typing import TypedDict
from langgraph.graph import END, StateGraph
from agents.crewai_agent import create_crewai_agent
from agents.custom_openai_agent import generate_response
from agents.langchain_agent import create_langchain_agent



class A2AState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    input: str
    task: str
    web_results: str
    final_response: str


def langchain_node(state: A2AState) -> dict:
    """Extract the core task from the original user input."""

    print("Initial state:", state)

    agent = create_langchain_agent()

    result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Extract the core task from the following request. "
                    "Do not answer it. Return only the task:\n\n"
                    f"{state['input']}"
                ),
            }
        ]
    }
)

    final_message = result["messages"][-1]
    extracted_task = final_message.content

    print("Extracted task:", extracted_task)

    return {"task": extracted_task}


def crewai_node(state: A2AState) -> dict:
    """Research the extracted task using CrewAI and Tavily."""

    print("CrewAI research task:", state["task"])

    crew = create_crewai_agent(
        task_description=state["task"]
    )

    result = crew.kickoff()

    return {"web_results": str(result)}


def openai_response_node(state: A2AState) -> dict:
    """Generate the final answer from the task and research."""

    prompt = (
        "Use the following web research to answer the task.\n\n"
        f"Task:\n{state['task']}\n\n"
        f"Web research:\n{state['web_results']}\n\n"
        "Provide a clear and concise final response."
    )

    response = generate_response(prompt)

    return {"final_response": response}


builder = StateGraph(A2AState)

builder.add_node("LangChainAgent", langchain_node)
builder.add_node("CrewAIAgent", crewai_node)
builder.add_node("OpenAIAgent", openai_response_node)

builder.set_entry_point("LangChainAgent")

builder.add_edge("LangChainAgent", "CrewAIAgent")
builder.add_edge("CrewAIAgent", "OpenAIAgent")
builder.add_edge("OpenAIAgent", END)

graph = builder.compile()


if __name__ == "__main__":
    input_text = (
        "Can you summarize the latest trends in GenAI "
        "for enterprise?"
    )

    output = graph.invoke({"input": input_text})

    print("\nFinal Output:\n")
    print(output["final_response"])