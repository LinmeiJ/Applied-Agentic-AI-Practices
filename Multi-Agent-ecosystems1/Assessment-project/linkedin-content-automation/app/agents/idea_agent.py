from autogen_agentchat.agents import AssistantAgent

from app.model_client import create_model_client


def create_idea_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for generating
    LinkedIn content ideas.
    """

    return AssistantAgent(
        name="idea_agent",
        model_client=create_model_client(),
        system_message=(
            "You are an experienced LinkedIn content strategist. "
            "Generate creative, engaging, and professional LinkedIn "
            "post ideas based on the user's topic."
        ),
    )