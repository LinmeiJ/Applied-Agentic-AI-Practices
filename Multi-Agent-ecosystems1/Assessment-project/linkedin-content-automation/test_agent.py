#AutoGen also communicates with Azure OpenAI over HTTP, which is an I/O operation.
#Instead of blocking while waiting for Azure to respond, Python can do other work.
import asyncio 
from app.agents.idea_agent import create_idea_agent


async def main():
    agent = create_idea_agent()
    result = await agent.run(
        task="Generate three LinkedIn post ideas about Agentic AI in software development."
    )
    print(result.messages[-1].content)

#asyncio.run() creates one, runs your async function, and then shuts it down.
#It’s similar to having a main() method in Java that starts your application.
if __name__ == "__main__":
    asyncio.run(main())