"""Create the CrewAI web research agent."""

import os

from crewai import Agent, Crew, LLM, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


class ToolInput(BaseModel):
    question: str = Field(description="Search query")


class SearchTool(BaseTool):
    name: str = "Search tool"
    description: str = (
        "Use this tool to find current information required for a query."
    )
    args_schema: type = ToolInput

    def _run(self, question: str) -> str:
        """Search the web using Tavily."""

        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is missing from the environment.")

        web_search = TavilySearchResults(
            tavily_api_key=TAVILY_API_KEY
        )

        result = web_search.invoke({"query": question})
        return str(result)


def create_crewai_agent(task_description: str) -> Crew:
    """Create a CrewAI research crew for the supplied task."""

    llm = LLM(
        model=f"azure/{os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT']}",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"], 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"], 
        is_litellm=True,
    )

    researcher = Agent(
        role="Researcher",
        goal="Search the web and gather information",
        backstory="Expert in web research using advanced techniques",
        tools=[SearchTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    task = Task(
        description=(
            "Research this briefly and return five bullet points only: "
            f"{task_description}"
        ),
        expected_output=(
            "Five short bullet points with the most relevant findings."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
    )

    return crew