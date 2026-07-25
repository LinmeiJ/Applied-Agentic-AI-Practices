from .models import LinkedInRequest, LinkedInResponse
from app.agents.idea_agent import create_idea_agent
from app.agents.writer_agent import create_writer_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.agents.hashtag_agent import create_hashtag_agent


class LinkedInService:

    async def generate_post(
        self,
        request: LinkedInRequest,
    ) -> LinkedInResponse:

        topic = request.context.topic

        ideas = await generate_linkedin_ideas(topic)

        draft = await generate_linkedin_draft(
            request,
            ideas,
        )

        reviewed_draft = await review_linkedin_post(
            request,
            draft,
        )

        hashtags = await generate_hashtags(
            reviewed_draft,
        )

        return LinkedInResponse(
            ideas=[ideas],
            draft=reviewed_draft,
            confidence=0.85,
            hashtags=hashtags,
            status="generated",
        )



async def generate_linkedin_ideas(topic: str) -> str:
    """
    Generate LinkedIn post ideas for the provided topic.
    """

    idea_agent = create_idea_agent()

    # Send the changing user topic to the agent.
    result = await idea_agent.run(
        task=f"Generate three LinkedIn post ideas about {topic}."
    )

    return result.messages[-1].content



async def generate_linkedin_draft(
    request: LinkedInRequest,
    ideas_text: str,
) -> str:
    """
    Generate one LinkedIn post using the request details
    and the ideas produced by the Idea Agent.
    """

    writer_agent = create_writer_agent()

    task = f"""
Write one LinkedIn post using the information below.

Company: {request.brand.company_name}
Industry: {request.brand.industry}
Brand voice: {request.brand.brand_voice}
Target audience: {request.brand.target_audience}

Topic: {request.context.topic}
Goal: {request.context.goal}
Key points: {request.context.key_points}

Generated ideas:
{ideas_text}
"""

    result = await writer_agent.run(task=task)

    return result.messages[-1].content



async def review_linkedin_post(
    request: LinkedInRequest,
    draft: str,
) -> str:
    """
    Review and improve the LinkedIn draft.
    """

    reviewer_agent = create_reviewer_agent()

    task = f"""
Review the LinkedIn post below.

Brand voice:
{request.brand.brand_voice}

Target audience:
{request.brand.target_audience}

LinkedIn draft:
{draft}

Improve grammar, clarity, engagement, and professionalism.
Return only the improved post.
"""

    result = await reviewer_agent.run(task=task)

    return result.messages[-1].content



async def generate_hashtags(
    draft: str,
) -> list[str]:
    """
    Generate hashtags for the final LinkedIn post.
    """

    hashtag_agent = create_hashtag_agent()

    result = await hashtag_agent.run(
        task=f"""
Generate 4 to 6 professional LinkedIn hashtags for the following post.

{draft}
"""
    )

    hashtags = [
        tag.strip()
        for tag in result.messages[-1].content.split(",")
    ]

    return hashtags