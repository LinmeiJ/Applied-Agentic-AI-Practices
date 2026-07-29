from .models import LinkedInRequest, LinkedInResponse
from app.agents.idea_agent import create_idea_agent
from app.agents.writer_agent import create_writer_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.agents.hashtag_agent import create_hashtag_agent
from app.agents.evaluator_agent import create_evaluator_agent
import json

MAX_REVISIONS = 2

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

        confidence, confidence_reason = await evaluate_linkedin_post(
            request,
            reviewed_draft,
        )

        hashtags = await generate_hashtags(
            reviewed_draft,
        )

        # Normal response 
        return LinkedInResponse(
            ideas=[ideas],
            draft=reviewed_draft,
            confidence=confidence,  # Evaluated by evaluator_agent using weighted rubric
            confidence_reason=confidence_reason,
            minimum_confidence=request.automation.minimum_confidence,
            dry_run=request.automation.dry_run,
            hashtags=hashtags,
            status="generated",
            company=request.brand.company_name,
            goal=request.context.goal,
            topic=request.context.topic,
            audience=request.brand.target_audience,
            revision_number = request.revision_number,
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
                confidence_reason=(
                    "The post was not reevaluated because the maximum "
                    "revision limit was reached."
                ),
                minimum_confidence=request.automation.minimum_confidence,
                dry_run=request.automation.dry_run,
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
        
        # Use the writer agent with feedback
        writer_agent = create_writer_agent()
        
        task = f"""
            Revise the LinkedIn post below based on the reviewer's feedback.

            Company: {request.brand.company_name}
            Industry: {request.brand.industry}
            Brand voice: {request.brand.brand_voice}
            Target audience: {request.brand.target_audience}

            Topic: {request.context.topic}
            Goal: {request.context.goal}
            Key points: {request.context.key_points}

            Previous post:
            {request.previous_post}

            Reviewer feedback:
            {request.human_feedback}

            Revision number: {request.revision_number}

            Rewrite the post incorporating the feedback while maintaining:
            - Brand voice and tone
            - Key points
            - Engagement and clarity

            Return only the revised post.
            """
        
        result = await writer_agent.run(task=task)
        revised_draft = result.messages[-1].content


        # Then review it (polish) - this ensures quality
        reviewer_agent = create_reviewer_agent()
        
        review_task = f"""
            Review and polish the LinkedIn post below.

            Brand voice: {request.brand.brand_voice}
            Target audience: {request.brand.target_audience}

            LinkedIn draft:
            {revised_draft}

            Improve grammar, clarity, engagement, and professionalism.
            Return only the improved post.
            """
        
        review_result = await reviewer_agent.run(task=review_task)
        final_draft = review_result.messages[-1].content

        # Evaluate the final version
        confidence, confidence_reason = await evaluate_linkedin_post(
            request,
            final_draft,
        )

        hashtags = await generate_hashtags(revised_draft)

        return LinkedInResponse(
            ideas=[],
            draft=revised_draft,
            confidence=confidence,
            confidence_reason=confidence_reason,
            minimum_confidence=request.automation.minimum_confidence,
            dry_run=request.automation.dry_run,
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
    
# Weights should sum to 1.0. Tune these based on what matters most to the brand.
EVALUATION_WEIGHTS = {
    "grammar_readability": 0.06,
    "clarity": 0.08,
    "brand_voice_alignment": 0.12,
    "audience_alignment": 0.11,
    "key_point_coverage": 0.14,
    "engagement_potential": 0.10,
    "accessibility_and_relatability": 0.10,
    "visual_scannability": 0.08,
    "topic_relevance": 0.07,
    "leadership_tone_appropriateness": 0.14,
}


async def evaluate_linkedin_post(
    request: LinkedInRequest,
    draft: str,
) -> tuple[float, str]:
    """
    Evaluate the final LinkedIn post: bias/judgment acts as a hard gate,
    everything else is scored against a weighted rubric.
    """

    evaluator = create_evaluator_agent()

    task = f"""
        Evaluate the LinkedIn post below.

        Company:
        {request.brand.company_name}

        Industry:
        {request.brand.industry}

        Brand voice:
        {request.brand.brand_voice}

        Target audience:
        {request.brand.target_audience}

        Topic:
        {request.context.topic}

        Goal:
        {request.context.goal}

        Required key points:
        {request.context.key_points}

        Final LinkedIn post:
        {draft}
        """

    result = await evaluator.run(task=task)
    raw_response = result.messages[-1].content.strip()

    # Strip markdown code fences if present
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`")
        if raw_response.lower().startswith("json"):
            raw_response = raw_response[4:]
        raw_response = raw_response.strip()

    try:
        evaluation = json.loads(raw_response)

        bias_check = evaluation["bias_check"]
        if bias_check["contains_bias_or_judgment"]:
            return 0.0, (
                f"REJECTED - bias/judgment detected: {bias_check['explanation']}"
            )

        scores = evaluation["scores"]
        justifications = evaluation["justifications"]

        for criterion in EVALUATION_WEIGHTS:
            score = float(scores[criterion])
            if not (0.0 <= score <= 1.0):
                raise ValueError(f"{criterion} score {score} out of range")

        confidence = sum(
            float(scores[criterion]) * weight
            for criterion, weight in EVALUATION_WEIGHTS.items()
        )
        confidence = max(0.0, min(1.0, confidence))

        reason_parts = [
            f"{criterion} ({scores[criterion]:.2f}): {justifications[criterion]}"
            for criterion in EVALUATION_WEIGHTS
        ]
        confidence_reason = " | ".join(reason_parts)

        return confidence, confidence_reason

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Evaluator response could not be parsed: {error}")
        print(f"Raw evaluator response: {raw_response}")
        return 0.0, "The evaluator returned an invalid response."

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




