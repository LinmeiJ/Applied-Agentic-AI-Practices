
### Create a LangChain agent with a custom tool to extract tasks from user input.
import os
from dotenv import load_dotenv

from unittest import result
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import AzureChatOpenAI # imports the LangChain connector for Azure OpenAI.



@tool #this tool decorator transforms the function into something the LLM can understand and call.
def extract_task_from_input(input_text: str) -> str:
    """Extract the core task from user input."""
    return f"Extracted task from input: {input_text.strip()}"

def create_langchain_agent():
    llm = AzureChatOpenAI( 
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],   # gpt-5-mini 
        api_key=os.environ["AZURE_OPENAI_API_KEY"], 
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],    # APIM gateway endpoint 
        api_version=os.environ["AZURE_OPENAI_API_VERSION"], 
        temperature=1   
    )   
    return create_agent(
        model=llm,
        tools=[extract_task_from_input],
        system_prompt=(
            "Your only job is to extract the user's core task. "
            "Do not answer the task. "
            "Call extract_task_from_input, then return one short sentence "
            "describing what needs to be done."
        ),
    )