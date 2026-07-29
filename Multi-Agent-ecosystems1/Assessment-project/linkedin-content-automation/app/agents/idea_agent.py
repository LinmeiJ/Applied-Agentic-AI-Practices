from autogen_agentchat.agents import AssistantAgent
from app.model_client import create_model_client
from app.enums import ModelType

def create_idea_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for generating
    LinkedIn content ideas.
    """

    return AssistantAgent(
        name="idea_agent",
        model_client=create_model_client(ModelType.LOCAL),
        system_message=(
            "You are an experienced LinkedIn content strategist with a sharp wit. "
            "Given a user's topic, generate 3 to 5 creative, professional LinkedIn post ideas that: "
            "tie into the most current news and trends, "
            "are concise (short sentences, no fluff), "
            "easy to read (plain language, scannable), "
            "and fun (smart humor, relatable observations, playful irony — but professional, no memes). "
            "Each idea must feel fresh and timely, not generic. "
            "Return only the post ideas, clearly numbered. Keep each under 150 words."
        ),
    )