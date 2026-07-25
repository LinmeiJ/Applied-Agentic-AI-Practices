import asyncio 
import os 
from autogen_core.models import UserMessage 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient 
from dotenv import load_dotenv

load_dotenv() 
 
async def main(): 
    model_client = AzureOpenAIChatCompletionClient(
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        model="gpt-5-mini",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],   
        api_version="2024-10-21",
    )

    response = await model_client.create([ 
        UserMessage( 
            content="What is Microsoft AutoGen?", 
            source="user" 
        ) 
    ]) 
 
    print(response.content) 
 
    await model_client.close() 
 
 
if __name__ == "__main__": 
    asyncio.run(main()) 