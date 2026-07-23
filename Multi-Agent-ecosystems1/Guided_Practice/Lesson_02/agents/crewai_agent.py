"""Create the CrewAI web research agent."""
## Receive the extracted task, search the web, and return five researched bullet points.

import os

from crewai import Agent, Crew, LLM, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# define search-tool input.  It defines the input structure expected by the search tool.
class ToolInput(BaseModel):
    question: str = Field(description="Search query") # only one field: question.  The type is a string


class SearchTool(BaseTool):
    name: str = "Search tool" # The name presented by the AI agent
    description: str = (
        "Use this tool to find current information required for a query."
    )
    args_schema: type = ToolInput # This connects the tool to the input schema defined earlier. and it tells crewAI that the tools accepts: Json{"question": "...""}

    # _run() contains the actual tool behavior.CrewAI calls this method when the agent chooses the search tool. 
    # self refers to the tool object itself.
    # question is the query chosen by the LLM.
    def _run(self, question: str) -> str: 

        if not TAVILY_API_KEY: # Checks whether the API key is missing or empty.
            raise ValueError("TAVILY_API_KEY is missing from the environment.")

        # Creates the Tavily search client and passes the API key for authentication.
        web_search = TavilySearchResults(
            tavily_api_key=TAVILY_API_KEY
        )

        # Sends the search query to Tavily.
        result = web_search.invoke({"query": question}) # Tavily accepts 'query' so this line translates 'question' json to 'query'
        return str(result) # Tavily returns structured Python data, normally a list of search results and also gets converted to a string so CrewAI can included it in the agent's context.



"""This factory function creates a complete Crew."""
# It accepts the extracted task as a string.
# It returns a Crew object.

def create_crewai_agent(task_description: str) -> Crew:
    """Create a CrewAI research crew for the supplied task."""

    llm = LLM(
        model=f"azure/{os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT']}",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"], 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"], 
        is_litellm=True, # Indicates LiteLLM-style handling (LiteLLM is used in crewAI internally, so this line is not necesssary. LiteLLM: a translation layer, allowing developers to call models from OpenAI, Anthropic, Google Gemini, AWS Bedrock, and Azure using a single, standardized format; an AI gateway and Python library)
    )
    
    """ Define the researcher agent"""
    """Enables the detailed terminal output you saw, including:

        * Crew started
        * Agent started
        * Tool execution
        * Final answer

       Without verbose mode, the console would be much quieter.
    """
    researcher = Agent(
        role="Researcher",
        goal="Search the web and gather information",
        backstory="Expert in web research using advanced techniques",
        tools=[SearchTool()], # Creates an instance of the custom search tool and gives it to the agent.
        llm=llm,
        verbose=True,
        allow_delegation=False, #Prevents this agent from assigning work to another agent. but there is only one agent, so this may not be necessary.
    )
    
    # Creates the assignment for the researcher.
    # If task_description is "Summarize the latest trends in generative AI for enterprise."
    # Then the full task becomes: Research this briefly and return five bullet points only: Summarize the latest trends in generative AI for enterprise.
    task = Task(
        description=(
            "Research this briefly and return five bullet points only: "
            f"{task_description}"
        ),
        expected_output=( #This tells CrewAI what successful output should look like.
            "Five short bullet points with the most relevant findings."
        ),
        agent=researcher, # Assigns this task to the researcher agent.
    )

    # build and return the crew
    crew = Crew(     # Creates the CrewAI execution container.
        agents=[researcher], # Lists all agents that belong to the crew.
        tasks=[task], # Lists all tasks that should be executed.
        verbose=True, # Enables the detailed Crew-level logs. That is why both the agent and the crew printed status boxes.
    )

    return crew # Returns the configured crew to main.py.