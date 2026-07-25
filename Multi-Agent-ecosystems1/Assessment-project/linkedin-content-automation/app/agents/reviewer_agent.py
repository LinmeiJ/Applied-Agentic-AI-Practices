from autogen_agentchat.agents import AssistantAgent

from app.model_client import create_model_client


def create_reviewer_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for reviewing
    and improving the LinkedIn draft.
    """

    return AssistantAgent(
        name="reviewer_agent",
        model_client=create_model_client(),
        system_message=(
            "You are a professional LinkedIn content reviewer. "
            "Review the provided LinkedIn post for clarity, tone, "
            "professionalism, engagement, and brand alignment. "
            "Return an improved final version of the post only."
        ),
    )