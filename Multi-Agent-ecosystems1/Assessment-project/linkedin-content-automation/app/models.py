from pydantic import BaseModel, Field

# Like These are your shared DTOs
#...BaseModel) topic, audience, tone, and context is like private variables in a java class
#... Field(...) adds validation and documentation, simiar to @Size(min=2) annotation in Java


class BrandConfig(BaseModel):
    """
    Brand-specific configuration used when generating
    LinkedIn content.
    """
    company_name: str = Field(
        min_length=2,
        description="Name of the company or brand",
    )

    industry: str = Field(
        min_length=2,
        description="Industry in which the company operates",
    )

    brand_voice: str = Field(
        default="professional and informative",
        description="Writing style and tone for the LinkedIn post",
    )

    target_audience: str = Field(
        min_length=2,
        description="The intended audience for the post",
    )



class ContentContext(BaseModel):
    """
    Describes the content that should be generated.
    """
    topic: str = Field(
        min_length=3,
        description="The main topic of the LinkedIn post",
    )

    goal: str = Field(
        default="Educate and engage the audience",
        description="The purpose of the LinkedIn post",
    )

    key_points: list[str] = Field(
        default_factory=list,
        description="Important points that should appear in the post",
    )

    revision_number: int = Field(
        default=0,
        description="Track revision number when human reviewer requested a revision",
    )



class AutomationConfig(BaseModel):
    minimum_confidence: float = Field(
        default=0.80,
        ge=0,
        le=1,
        description="Minimum confidence required for automatic publishing",
    )

    dry_run: bool = Field(
        default=True,
        description="When true, route the post for review instead of publishing",
    )

class LinkedInResponse(BaseModel):
    ideas: list[str]
    draft: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    hashtags: list[str]
    status: str
    company: str
    goal: str
    topic: str
    audience: str
    revision_number: int = Field(
        default=0,
        description="Revision iteration number for this response.",
)

class LinkedInRequest(BaseModel):
    brand: BrandConfig
    context: ContentContext
    automation: AutomationConfig = Field(
        default_factory=AutomationConfig,
    )

    revise: bool = Field(
        default=False,
        description="Whether this request is revising an existing post.",
    )

    previous_post: str | None = Field(
        default=None,
        description="The previous LinkedIn post to revise.",
    )

    human_feedback: str | None = Field(
        default=None,
        description="Feedback provided by the reviewer.",
    )

    reviewer_name: str | None = Field(
        default=None,
        description="Name or email of the reviewer.",
    )

    revision_number: int = Field(
        default=0,
        ge=0,
        description="Revision iteration number.",
    )