"""Integrate the agents using LangGraph."""
### Run me via CLI: python main.py

from typing import TypedDict # TypedDict lets you describe the structure of a Python dictionary. the workflow passes one shared dictionary between nodes.

# StateGraph:Creates a graph whose nodes pass a shared state dictionary between one another.
# End: Represents the end of the workflow.
from langgraph.graph import END, StateGraph
from agents.crewai_agent import create_crewai_agent # Imports the factory function that builds your CrewAI researcher.
from agents.custom_openai_agent import generate_response # Imports the function that generates the polished final response.
from agents.langchain_agent import create_langchain_agent # Imports the factory function that builds your LangChain task-extraction agent.


# This defines the shared workflow state. Each node reads from this shared dictionary and adds new values to it.

class A2AState(TypedDict, total=False): #Normally, a TypedDict expects every declared key to exist. But your workflow does not have every key at the beginning. so set total = false (means: all keys are optional while the graph is running.)
    """Shared state passed between LangGraph nodes."""

    input: str
    task: str
    web_results: str
    final_response: str

#This defines the first LangGraph node. It receives the current shared state.
def langchain_node(state: A2AState) -> dict:
    """Extract the core task from the original user input.""" # This node’s responsibility is task extraction.It should not research or answer the question.

    print("Initial state:", state) # This line is not required for the graph to work. It only helps you observe the flow.

    # Calls the factory function from langchain_agent.py. 
    # this function creates and returns a LangChain agent configured with:  Azure OpenAI, a system prompt, the extraction tool
    # The local variable agent now refers to that runnable LangChain agent.
    agent = create_langchain_agent() 

    result = agent.invoke( # invoke() runs the agent once, It sends input to the agent and waits for the complete result.
    {
        "messages": [ # The agent expects chat messages.The input is a dictionary containing a messages list.
            {
                "role": "user",
                "content": (
                    "Extract the core task from the following request. "
                    "Do not answer it. Return only the task:\n\n"
                    f"{state['input']}" # This inserts the original user input from the shared state.
                ),
            }
        ]
    }
)

    final_message = result["messages"][-1] # This gets the last message in the returned messages list.
    extracted_task = final_message.content # Reads the text content from the final message.

    print("Extracted task:", extracted_task)

    return {"task": extracted_task} # Returns only the new state update.LangGraph merges this into the existing state.

# This defines the second node. 
def crewai_node(state: A2AState) -> dict:
    """Research the extracted task using CrewAI and Tavily."""

    print("CrewAI research task:", state["task"]) # Prints the task passed into CrewAI.

    crew = create_crewai_agent( # Calls the CrewAI factory function.
        task_description=state["task"] # Passes the extracted task into the CrewAI configuration. This is one of the agent-to-agent connections.
    )

    result = crew.kickoff() # this kicks off the crewai agent

    return {"web_results": str(result)} # Converts the CrewAI result to a string and adds it to the shared state.

# This defines the third and final processing node.
def openai_response_node(state: A2AState) -> dict:
    """Generate the final answer from the task and research."""

    prompt = ( # Starts constructing a single prompt string. Tells the LLM to base its answer on the research.
        "Use the following web research to answer the task.\n\n"
        f"Task:\n{state['task']}\n\n" # Adds the extracted task.
        f"Web research:\n{state['web_results']}\n\n" # Adds the CrewAI research findings.
        "Provide a clear and concise final response." # Gives the output-style instruction.
    )

    response = generate_response(prompt) # Calls the function from custom_openai_agent.py. that function: 1. Creates an Azure LLM connection. 2. Sends this prompt to the model. 3.Returns the response string.

    return {"final_response": response} # Adds the final response to the shared state.


""" Create the graph builder """
builder = StateGraph(A2AState) # Creates a LangGraph workflow builder.It uses A2AState as the shared state structure.At this point, the graph is empty.No nodes or connections exist yet.

# Register each agent/node
builder.add_node("LangChainAgent", langchain_node) 
builder.add_node("CrewAIAgent", crewai_node)
builder.add_node("OpenAIAgent", openai_response_node)

builder.set_entry_point("LangChainAgent") # Tells LangGraph where execution begins. Without an entry point, LangGraph would not know which node to run first.

builder.add_edge("LangChainAgent", "CrewAIAgent") #Creates a fixed connection:LangChainAgent → CrewAIAgent (After task extraction finishes, research begins.)
builder.add_edge("CrewAIAgent", "OpenAIAgent") # then CrewAIAgent → OpenAIAgent
builder.add_edge("OpenAIAgent", END) # After OpenAIAgent final completes, stop the graph/workflow

graph = builder.compile() # Transforms the graph definition into an executable object.Before compilation, builder is the graph design.After compilation, graph can be invoked.


if __name__ == "__main__": # this checks whether the file is being executed directly. when "python main.py", Python sets: __name__ == "__main__", so this block runs.
    input_text = (
        "Can you summarize the latest trends in GenAI "
        "for enterprise?"
    )

    output = graph.invoke({"input": input_text}) # This starts the entire LangGraph workflow.

    print("\nFinal Output:\n") # Prints a heading with blank lines before and after.
    print(output["final_response"]) # Reads only the final response from the completed state and prints it.It does not print the entire dictionary.To inspect everything, you could temporarily use:print(output), That would show all four state values.