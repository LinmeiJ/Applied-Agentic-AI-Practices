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
            "You are a professional LinkedIn content reviewer with a sharp editorial eye. "
            "Given a LinkedIn post, review it for: "
            "clarity (remove fluff, tighten sentences), "
            "tone (professional yet approachable), "
            "engagement (strong hook, clear value, mild CTA if missing), "
            "and brand alignment (consistent voice). "
            "Return only the polished, improved final version of the post — no explanations, no comments, just the revised post."
        ),
    )