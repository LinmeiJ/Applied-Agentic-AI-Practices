from autogen_agentchat.agents import AssistantAgent
from app.model_client import create_model_client
from app.enums import ModelType


def create_hashtag_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for generating
    relevant LinkedIn hashtags.
    """

    return AssistantAgent(
        name="hashtag_agent",
        model_client=create_model_client(ModelType.LOCAL),
        system_message=(
            "You are a LinkedIn hashtag strategist."
            "Given a LinkedIn post, generate 4 to 6 relevant, high-impact hashtags that are professional, industry-appropriate, and likely to increase discoverability."
            "Return only the hashtags, separated by commas."
            "You may include one subtle, professional emoji (e.g., 📊, 💡, 🚀) if it enhances relevance—but avoid overdoing it. Keep the tone polished, "
            "LinkedIn-friendly, and never gimmicky."
        ),
    )