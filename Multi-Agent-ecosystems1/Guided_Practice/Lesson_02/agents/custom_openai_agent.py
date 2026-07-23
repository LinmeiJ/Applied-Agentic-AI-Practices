"""Generate the final response using an Azure-hosted LLM."""
# It is primarily a simple LLM wrapper, not really an agent.
# Responsibility: Take the task plus CrewAI research and turn them into a polished final response.

import os

from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

 
def create_llm() -> LLM: # Defines a factory function that creates and returns an LLM object.
    """Create the Azure OpenAI LLM connection."""

    return LLM( # Creates and immediately returns the LLM connection.
        model=f"azure/{os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT']}",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"], 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"], 
        is_litellm=True,
    )

## Defines a function that accepts one prompt string and returns one response string.
def generate_response(prompt: str) -> str:
    """Generate a final response for the supplied prompt."""

    llm = create_llm() # Creates the Azure LLM connection. This happens each time generate_response() is called.
    response = llm.call(prompt) # Sends the prompt directly to the LLM. This is a plain model call.

    return str(response) # Converts the model result into a regular Python string and returns it to main.py