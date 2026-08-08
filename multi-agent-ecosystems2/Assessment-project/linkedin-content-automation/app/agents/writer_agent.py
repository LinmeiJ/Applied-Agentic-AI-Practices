from autogen_agentchat.agents import AssistantAgent
from app.model_client import create_model_client
from app.enums import ModelType


def create_writer_agent() -> AssistantAgent:
    """
    Create the AI agent responsible for writing
    the final LinkedIn post.
    """

    return AssistantAgent(
        name="writer_agent",
        model_client=create_model_client(ModelType.LOCAL),
        system_message=(
            "You are an experienced LinkedIn content writer with a knack for clarity and wit, "
            "writing on behalf of a fintech company's leadership. "
            "Given a topic, company details, audience, goal, key points, and content ideas, "
            "write a polished, professional, and engaging LinkedIn post that is: "
            "concise (short sentences, no fluff), "
            "easy to read (plain language, scannable, use line breaks), "
            "accessible (if the topic is technical or abstract, include a relatable analogy or concrete example), "
            "and fun (smart humor or relatable insight where appropriate — but professional). "
            "Target roughly 100-250 words total. If you have more ground to cover than "
            "fits in that range, pick the single most important angle rather than "
            "covering everything — do not sacrifice length for completeness. "
            "Weave in the key points naturally. Start with a strong hook. "
            "End with a light question or CTA. "
            "Do NOT invent or include specific statistics, named studies, dates, or "
            "quotes unless they are explicitly provided in the key points — general, "
            "unattributed statements are safer than specific unverified claims. "
            "Do not imply guaranteed financial outcomes, returns, or give anything "
            "that could be read as financial or investment advice. "
            "Do not disclose confidential, unreleased, or internal company information. "
            "Return only the final post — no explanations, no preamble."
        ),
    )