from .models import LinkedInRequest, LinkedInResponse
from app.agents.idea_agent import create_idea_agent
from app.agents.writer_agent import create_writer_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.agents.hashtag_agent import create_hashtag_agent
from app.agents.evaluator_agent import create_evaluator_agent
import json
import asyncio
from datetime import datetime
from typing import Optional, Tuple
import asyncio

# module-level, shared across requests
_ollama_lock = asyncio.Lock()


MAX_REVISIONS = 3
AI_DISCLOSURE = (
    "\n\n🤖 This post was drafted by a 5-agent AI system "
    "(idea, writer, reviewer, evaluator, hashtag) and reviewed by a human before publishing."
)

# ==================== ERROR HANDLING UTILITIES ====================

class AgentError(Exception):
    """Custom exception for agent failures"""
    pass

async def safe_agent_call(agent_func, *args, **kwargs) -> Optional[str]:
    """
    Safely call an agent with error handling and retry logic.
    Returns the agent's response or None if failed.
    """
    max_retries = 2
    retry_delay = 2  # seconds
    func_name = agent_func.__name__ if hasattr(agent_func, '__name__') else str(agent_func)

    for attempt in range(max_retries + 1):
        try:
            print(f"🔄 Calling agent: {func_name} (attempt {attempt + 1}/{max_retries + 1})")
            result = await agent_func(*args, **kwargs)

            # Validate response
            if result is None:
                raise ValueError("Agent returned None")
            if isinstance(result, str) and len(result.strip()) < 10:
                raise ValueError(f"Agent response too short: {len(result)} characters")

            print(f"✅ Agent {func_name} succeeded")
            return result

        except Exception as e:
            print(f"❌ Agent {func_name} failed (attempt {attempt + 1}): {e}")

            if attempt < max_retries:
                print(f"⏳ Retrying {func_name} in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"💥 Agent {func_name} failed after {max_retries + 1} attempts")
                raise AgentError(f"Agent {func_name} failed: {str(e)}")

    return None

def log_error(error_type: str, error_message: str, context: dict = None):
    """
    Log errors for monitoring and debugging.
    In production, this could write to a database or external logging service.
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "error_type": error_type,
        "error_message": error_message,
        "context": context or {}
    }
    print(f"📋 ERROR LOG: {json.dumps(log_entry, indent=2)}")

    # TODO: In production, send this to Google Sheets or a logging service
    # For now, we just print it

# ==================== MAIN SERVICE CLASS ====================

class LinkedInService:
    async def generate_post(self, request: LinkedInRequest,) -> LinkedInResponse:
        async with _ollama_lock:

            """
            Generate a LinkedIn post with full error handling.
            """
            print(f"🚀 Starting post generation at {datetime.now().isoformat()}")
            print(f"📨 Request: revise={request.revise}, topic={request.context.topic}")

            try:
                # This part is for revision flow
                if request.revise:
                    print("🔄 Revision flow detected")
                    return await self._revise_post(request)

                # STEP 1: Generate ideas
                try:
                    topic = request.context.topic
                    ideas = await safe_agent_call(generate_linkedin_ideas, topic)
                    if ideas is None:
                        ideas = "1. AI is transforming fintech\n2. The future of financial planning\n3. Why data-driven decisions win"
                        log_error("FALLBACK", "Ideas agent failed, using fallback ideas")
                except AgentError as e:
                    ideas = "1. AI is transforming fintech\n2. The future of financial planning\n3. Why data-driven decisions win"
                    log_error("AGENT_FAILURE", f"Idea agent failed: {str(e)}", {"topic": topic})

                # STEP 2: Generate draft
                try:
                    draft = await safe_agent_call(generate_linkedin_draft, request, ideas)
                    if draft is None:
                        draft = f"Exciting developments in {request.context.topic} are reshaping the fintech landscape. At {request.brand.company_name}, we're seeing firsthand how AI and data analytics are transforming financial planning. The future is here, and it's data-driven. #Fintech #Innovation"
                        log_error("FALLBACK", "Draft agent failed, using fallback draft")
                except AgentError as e:
                    draft = f"Exciting developments in {request.context.topic} are reshaping the fintech landscape. At {request.brand.company_name}, we're seeing firsthand how AI and data analytics are transforming financial planning. The future is here, and it's data-driven. #Fintech #Innovation"
                    log_error("AGENT_FAILURE", f"Writer agent failed: {str(e)}", {"topic": request.context.topic})

                # STEP 3: Review draft
                try:
                    reviewed_draft = await safe_agent_call(review_linkedin_post, request, draft)
                    if reviewed_draft is None:
                        reviewed_draft = draft
                        log_error("FALLBACK", "Reviewer agent failed, using original draft")
                except AgentError as e:
                    reviewed_draft = draft
                    log_error("AGENT_FAILURE", f"Reviewer agent failed: {str(e)}", {"draft_length": len(draft)})

                # Append AI disclosure once, right after review is finalized.
                # Everything downstream (evaluation, hashtags, response) uses
                # final_draft so the disclosure is part of what actually gets
                # scored and published.
                final_draft = reviewed_draft + AI_DISCLOSURE

                # STEP 4: Evaluate post
                try:
                    confidence, confidence_reason = await safe_agent_call(
                        evaluate_linkedin_post, request, final_draft
                    )
                    if confidence is None:
                        confidence = 0.5  # Neutral fallback
                        confidence_reason = "Evaluation agent failed, using neutral confidence"
                        log_error("FALLBACK", "Evaluator agent failed, using default confidence")
                except AgentError as e:
                    confidence = 0.5
                    confidence_reason = f"Evaluation agent failed: {str(e)}"
                    log_error("AGENT_FAILURE", f"Evaluator agent failed: {str(e)}", {"draft_length": len(final_draft)})

                # STEP 5: Generate hashtags
                try:
                    hashtags = await safe_agent_call(generate_hashtags, final_draft)
                    if hashtags is None or len(hashtags) == 0:
                        hashtags = ["#Fintech", "#Innovation", "#FutureOfFinance"]
                        log_error("FALLBACK", "Hashtag agent failed, using fallback hashtags")
                except AgentError as e:
                    hashtags = ["#Fintech", "#Innovation", "#FutureOfFinance"]
                    log_error("AGENT_FAILURE", f"Hashtag agent failed: {str(e)}", {"draft_length": len(final_draft)})

                print(f"✅ Post generation completed at {datetime.now().isoformat()}")
                print(f"📊 Confidence: {confidence:.2f}, Hashtags: {len(hashtags)}")

                # Normal response
                return LinkedInResponse(
                    ideas=[ideas],
                    draft=final_draft,
                    confidence=confidence,
                    confidence_reason=confidence_reason,
                    minimum_confidence=request.automation.minimum_confidence,
                    dry_run=request.automation.dry_run,
                    hashtags=hashtags,
                    status="AI_GENERATED",
                    company=request.brand.company_name,
                    goal=request.context.goal,
                    topic=request.context.topic,
                    audience=request.brand.target_audience,
                    revision_number=request.revision_number,
                    # Decision logic omitted for now (per your request)
                    decision=None,
                    reject_reason=None,
                )

            except Exception as e:
                # Catch-all for unexpected errors
                print(f"💥 UNEXPECTED ERROR in generate_post: {e}")
                log_error("UNEXPECTED", str(e), {"request": request.model_dump_json()})

                # Return a degraded but functional response
                return LinkedInResponse(
                    ideas=["Unable to generate ideas at this time"],
                    draft=f"We encountered an error while generating your post. Please try again later.\n\nError: {str(e)}",
                    confidence=0.0,
                    confidence_reason=f"Generation failed: {str(e)}",
                    minimum_confidence=request.automation.minimum_confidence,
                    dry_run=request.automation.dry_run,
                    hashtags=["#Error", "#PleaseRetry"],
                    status="ERROR",
                    company=request.brand.company_name,
                    goal=request.context.goal,
                    topic=request.context.topic,
                    audience=request.brand.target_audience,
                    revision_number=request.revision_number,
                    decision="reject",
                    reject_reason=f"System error: {str(e)}",
                )

    async def _revise_post(
        self,
        request: LinkedInRequest,
    ) -> LinkedInResponse:
        """
        Revise an existing LinkedIn post with full error handling.
        """
        print(f"🔄 Starting revision at {datetime.now().isoformat()}")
        print(f"📨 Revision number: {request.revision_number}, MAX: {MAX_REVISIONS}")

        try:
            # Check revision limit
            if request.revision_number >= MAX_REVISIONS:
                print(f"⛔ Revision limit exceeded: {request.revision_number} >= {MAX_REVISIONS}")
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
                    status="AI_REJECTED",
                    company=request.brand.company_name,
                    goal=request.context.goal,
                    topic=request.context.topic,
                    audience=request.brand.target_audience,
                    revision_number=request.revision_number,
                    decision="reject",
                    reject_reason="System rejection: Revision limit exceeded",
                )

            # STEP 1: Use writer agent to revise with feedback
            try:
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

                if not revised_draft or len(revised_draft.strip()) < 10:
                    raise ValueError("Writer agent returned insufficient content")

                print(f"✅ Writer agent revision succeeded: {len(revised_draft)} characters")

            except Exception as e:
                print(f"❌ Writer agent revision failed: {e}")
                log_error("REVISION_FAILURE", f"Writer agent failed: {str(e)}",
                         {"revision_number": request.revision_number})
                # Use previous post as fallback
                revised_draft = request.previous_post or f"Revision failed. Please try again.\n\nFeedback: {request.human_feedback}"

            # STEP 2: Polish with reviewer agent
            try:
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

                final_draft = review_result.messages[-1].content + AI_DISCLOSURE  # Append AI disclosure

                if not final_draft or len(final_draft.strip()) < 10:
                    # Fallback to unpolished version — still needs the disclosure
                    final_draft = revised_draft + AI_DISCLOSURE

                print(f"✅ Reviewer agent polishing succeeded: {len(final_draft)} characters")

            except Exception as e:
                print(f"❌ Reviewer agent polishing failed: {e}")
                log_error("REVISION_FAILURE", f"Reviewer agent failed: {str(e)}",
                         {"revision_number": request.revision_number})
                # Fallback — still needs the disclosure
                final_draft = revised_draft + AI_DISCLOSURE

            # STEP 3: Evaluate the final version
            try:
                confidence, confidence_reason = await safe_agent_call(
                    evaluate_linkedin_post, request, final_draft
                )
                if confidence is None:
                    confidence = 0.5
                    confidence_reason = "Evaluation failed during revision"
                    log_error("FALLBACK", "Evaluator failed during revision")
            except AgentError as e:
                confidence = 0.5
                confidence_reason = f"Evaluation during revision failed: {str(e)}"
                log_error("AGENT_FAILURE", f"Evaluator failed during revision: {str(e)}")

            # STEP 4: Generate hashtags
            try:
                hashtags = await safe_agent_call(generate_hashtags, final_draft)
                if hashtags is None or len(hashtags) == 0:
                    hashtags = ["#Fintech", "#Innovation", "#FutureOfFinance"]
                    log_error("FALLBACK", "Hashtag agent failed during revision")
            except AgentError as e:
                hashtags = ["#Fintech", "#Innovation", "#FutureOfFinance"]
                log_error("AGENT_FAILURE", f"Hashtag agent failed during revision: {str(e)}")

            print(f"✅ Revision completed at {datetime.now().isoformat()}")
            print(f"📊 Confidence after revision: {confidence:.2f}")

            return LinkedInResponse(
                ideas=[],
                draft=final_draft,
                confidence=confidence,
                confidence_reason=confidence_reason,
                minimum_confidence=request.automation.minimum_confidence,
                dry_run=request.automation.dry_run,
                hashtags=hashtags,
                status="AI_REVISED",
                company=request.brand.company_name,
                goal=request.context.goal,
                topic=request.context.topic,
                audience=request.brand.target_audience,
                revision_number=request.revision_number,
                decision=request.decision,  # Pass through human decision
                reject_reason=None,
            )

        except Exception as e:
            # Catch-all for unexpected errors in revision
            print(f"💥 UNEXPECTED ERROR in _revise_post: {e}")
            log_error("UNEXPECTED", str(e), {"request": request.model_dump_json()})

            return LinkedInResponse(
                ideas=[],
                draft=request.previous_post or f"Revision failed: {str(e)}",
                confidence=0.0,
                confidence_reason=f"Revision failed: {str(e)}",
                minimum_confidence=request.automation.minimum_confidence,
                dry_run=request.automation.dry_run,
                hashtags=["#Error", "#PleaseRetry"],
                status="ERROR",
                company=request.brand.company_name,
                goal=request.context.goal,
                topic=request.context.topic,
                audience=request.brand.target_audience,
                revision_number=request.revision_number,
                decision="reject",
                reject_reason=f"System error during revision: {str(e)}",
            )

# ==================== AGENT FUNCTIONS ====================

# Weights should sum to 1.0. Tune these based on what matters most to the brand.
# These 10 keys must exactly match the "scores"/"justifications" keys in
# evaluator_agent.py's system_message JSON schema - if you edit the rubric
# there, mirror the change here too, or the schema-mismatch check below will
# raise instead of silently under/over-weighting the score.
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
) -> Tuple[float, str]:
    """
    Evaluate the final LinkedIn post: bias/judgment acts as a hard gate,
    everything else is scored against a weighted rubric.
    """
    try:
        evaluator = create_evaluator_agent()

        # Validate draft before evaluation
        if not draft or len(draft.strip()) < 10:
            raise ValueError(f"Draft too short for evaluation: {len(draft)} characters")

        # Truncate if too long (prevent token limit issues)
        MAX_DRAFT_LENGTH = 3000
        if len(draft) > MAX_DRAFT_LENGTH:
            draft = draft[:MAX_DRAFT_LENGTH] + "..."
            print(f"⚠️ Draft truncated to {MAX_DRAFT_LENGTH} characters for evaluation")

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

            Word count: {len(draft.split())}
            Character count: {len(draft)}

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

            expected_keys = set(EVALUATION_WEIGHTS)
            actual_keys = set(scores)
            if expected_keys != actual_keys:
                raise ValueError(
                    "Evaluator schema mismatch - "
                    f"missing from response: {expected_keys - actual_keys}, "
                    f"unexpected in response: {actual_keys - expected_keys}"
                )

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
            print(f"❌ Evaluator response parsing failed: {error}")
            print(f"📝 Raw response: {raw_response}")
            log_error("PARSING_ERROR", str(error), {"raw_response": raw_response[:500]})
            return 0.0, f"Evaluator returned invalid response: {str(error)}"

    except Exception as e:
        print(f"❌ Evaluator agent failed: {e}")
        log_error("EVALUATOR_ERROR", str(e), {"draft_length": len(draft)})
        return 0.0, f"Evaluation failed: {str(e)}"

async def generate_linkedin_ideas(topic: str) -> str:
    """
    Generate LinkedIn post ideas for the provided topic.
    """
    try:
        if not topic or len(topic.strip()) < 3:
            raise ValueError(f"Topic too short: {topic}")

        idea_agent = create_idea_agent()

        result = await idea_agent.run(
            task=f"Generate three LinkedIn post ideas about {topic}."
        )

        ideas = result.messages[-1].content
        if not ideas or len(ideas.strip()) < 20:
            raise ValueError("Idea agent returned insufficient content")

        return ideas

    except Exception as e:
        print(f"❌ Idea generation failed: {e}")
        log_error("IDEA_ERROR", str(e), {"topic": topic})
        raise  # Re-raise to be handled by the caller

async def generate_linkedin_draft(
    request: LinkedInRequest,
    ideas_text: str,
) -> str:
    """
    Generate one LinkedIn post using the request details
    and the ideas produced by the Idea Agent.
    """
    try:
        if not ideas_text or len(ideas_text.strip()) < 10:
            raise ValueError("Ideas text too short for draft generation")

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
        draft = result.messages[-1].content

        if not draft or len(draft.strip()) < 20:
            raise ValueError("Writer agent returned insufficient content")

        return draft

    except Exception as e:
        print(f"❌ Draft generation failed: {e}")
        log_error("DRAFT_ERROR", str(e), {
            "company": request.brand.company_name,
            "topic": request.context.topic
        })
        raise  # Re-raise to be handled by the caller

async def review_linkedin_post(
    request: LinkedInRequest,
    draft: str,
) -> str:
    """
    Review and improve the LinkedIn draft.
    """
    try:
        if not draft or len(draft.strip()) < 10:
            raise ValueError("Draft too short for review")

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
        reviewed_draft = result.messages[-1].content

        if not reviewed_draft or len(reviewed_draft.strip()) < 10:
            # If review failed, return original draft
            print("⚠️ Reviewer returned empty response, using original draft")
            return draft

        return reviewed_draft

    except Exception as e:
        print(f"❌ Review failed: {e}")
        log_error("REVIEW_ERROR", str(e), {"draft_length": len(draft)})
        # Return original draft as fallback
        return draft

async def generate_hashtags(
    draft: str,
) -> list[str]:
    """
    Generate hashtags for the final LinkedIn post.
    """
    try:
        if not draft or len(draft.strip()) < 10:
            raise ValueError("Draft too short for hashtag generation")

        hashtag_agent = create_hashtag_agent()

        result = await hashtag_agent.run(
            task=f"""
                Generate 4 to 6 professional LinkedIn hashtags for the following post.

                {draft}
            """
        )

        hashtags_raw = result.messages[-1].content
        hashtags = [
            tag.strip()
            for tag in hashtags_raw.split(",")
            if tag.strip()
        ]

        # Ensure we have at least 3 hashtags
        if len(hashtags) < 3:
            hashtags = ["#Fintech", "#Innovation", "#FutureOfFinance"]
            print("⚠️ Hashtag agent returned insufficient tags, using fallbacks")

        return hashtags[:6]  # Limit to 6 hashtags

    except Exception as e:
        print(f"❌ Hashtag generation failed: {e}")
        log_error("HASHTAG_ERROR", str(e), {"draft_length": len(draft)})
        return ["#Fintech", "#Innovation", "#FutureOfFinance"]  # Fallback