"""Generate the final response using an Azure-hosted LLM."""

import os

from crewai import LLM
from dotenv import load_dotenv

load_dotenv()


def create_llm() -> LLM:
    """Create the Azure OpenAI LLM connection."""

    return LLM(
        model=f"azure/{os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT']}",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"], 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"], 
        is_litellm=True,
    )


def generate_response(prompt: str) -> str:
    """Generate a final response for the supplied prompt."""

    llm = create_llm()
    response = llm.call(prompt)

    return str(response)