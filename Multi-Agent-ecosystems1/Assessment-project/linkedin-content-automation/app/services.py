from .models import LinkedInRequest, LinkedInResponse
from app.agents.idea_agent import create_idea_agent

class LinkedInService:

    async def generate_post(
        self,
        request: LinkedInRequest,
    ) -> LinkedInResponse:

        company_name = request.brand.company_name
        industry = request.brand.industry
        brand_voice = request.brand.brand_voice
        target_audience = request.brand.target_audience

        topic = request.context.topic
        goal = request.context.goal
        key_points = request.context.key_points

        ideas_text = await generate_linkedin_ideas(topic)
        draft = (
            f"{topic} is creating new opportunities across the "
            f"{industry} industry.\n\n"
            f"At {company_name}, we believe this topic is especially "
            f"important for {target_audience}.\n\n"
            f"Our goal is to {goal.lower()}."
        )

        if key_points:
            formatted_points = "\n".join(
                f"- {point}" for point in key_points
            )

            draft += (
                "\n\nKey considerations include:\n"
                f"{formatted_points}"
            )

        draft += (
            f"\n\nThis post uses a {brand_voice} brand voice."
        )

        return LinkedInResponse(
            ideas=[ideas_text],
            draft=draft,
            confidence=0.85,
            hashtags=[
                "#FinTech",
                "#Innovation",
                "#LinkedIn",
                "#ArtificialIntelligence",
            ],
            status="generated",
        )

# 
async def generate_linkedin_ideas(topic: str) -> str:
    """
    Generate LinkedIn post ideas for the provided topic.
    """

    # Creates the idea agent using the Azure OpenAI client
    idea_agent = create_idea_agent()

    result = await idea_agent.run( #Sends the changing user topic to the agent.
        task=f"Generate three LinkedIn post ideas about {topic}."
    )

    return result.messages[-1].content