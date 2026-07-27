from .models import LinkedInRequest, LinkedInResponse
from app.agents.idea_agent import create_idea_agent
from app.agents.writer_agent import create_writer_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.agents.hashtag_agent import create_hashtag_agent

MAX_REVISIONS = 1

class LinkedInService:
    async def generate_post(
        self,
        request: LinkedInRequest,
    ) -> LinkedInResponse:
       
       #This part is for revision flow
        if request.revise:                
            return await self._revise_post(request)

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
            confidence=0.9, #The confidence score is currently a fixed value used to demonstrate the approval-gate workflow. In a production implementation, this value would be generated dynamically by an evaluator or reviewer agent based on the quality of the generated content.
            hashtags=hashtags,
            status="generated",
            company=request.brand.company_name,
            goal=request.context.goal,
            topic=request.context.topic,
            audience=request.brand.target_audience,
            revision_number = request.revision_number,
            decision=request.decision,
        )
    

    async def _revise_post(
        self,
        request: LinkedInRequest,
    ) -> LinkedInResponse:
        """
        Revise an existing LinkedIn post using reviewer feedback.
        """
        print("=== Incoming _revise_post request ===")
        print(request.model_dump_json(indent=2))
        print("======================================")


        if request.revision_number >= MAX_REVISIONS:
            return LinkedInResponse(
                ideas=[],
                draft=request.previous_post or "",
                confidence=0.0,
                hashtags=[],
                status="generated",
                company=request.brand.company_name,
                goal=request.context.goal,
                topic=request.context.topic,
                audience=request.brand.target_audience,
                revision_number=request.revision_number,
                decision="reject",
                reject_reason=("System rejection: Revision limit exceeded"),
            )

        reviewer_agent = create_reviewer_agent()

        task = f"""
            Revise the LinkedIn post below based on the reviewer's feedback.

            Brand voice:
            {request.brand.brand_voice}

            Target audience:
            {request.brand.target_audience}

            Previous post:
            {request.previous_post}

            Reviewer feedback:
            {request.human_feedback}

            Reviewer number:
            {request.revision_number}

            Apply the feedback, and also improve grammar, clarity, engagement, and professionalism.
            Return only the revised post.
            """

        result = await reviewer_agent.run(task=task)
        revised_draft = result.messages[-1].content

        hashtags = await generate_hashtags(revised_draft)

        return LinkedInResponse(
            ideas=[],
            draft=revised_draft,
            confidence=0.9,
            hashtags=hashtags,
            status="revised",
            company=request.brand.company_name,
            goal=request.context.goal,
            topic=request.context.topic,
            audience=request.brand.target_audience,
            revision_number= request.revision_number,
            decision=request.decision,
            reject_reason=None,
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

