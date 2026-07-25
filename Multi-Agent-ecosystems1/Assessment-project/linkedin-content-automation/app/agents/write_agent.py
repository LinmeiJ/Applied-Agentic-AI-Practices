from autogen_agentchat.agents import AssistantAgent

from app.model_client import create_model_client


def create_writer_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for writing
    the final LinkedIn post.
    """

    return AssistantAgent(
        name="writer_agent",
        model_client=create_model_client(),
        system_message=(
            "You are an experienced LinkedIn content writer. "
            "Write a polished, professional, and engaging LinkedIn post "
            "based on the provided topic, company details, audience, goal, "
            "key points, and generated content ideas."
        ),
    )