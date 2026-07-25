from autogen_agentchat.agents import AssistantAgent

from app.model_client import create_model_client


def create_hashtag_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for generating
    relevant LinkedIn hashtags.
    """

    return AssistantAgent(
        name="hashtag_agent",
        model_client=create_model_client(),
        system_message=(
            "You are a LinkedIn hashtag specialist. "
            "Generate 4 to 6 relevant and professional hashtags "
            "based on the provided LinkedIn post. "
            "Return only the hashtags, separated by commas."
        ),
    )