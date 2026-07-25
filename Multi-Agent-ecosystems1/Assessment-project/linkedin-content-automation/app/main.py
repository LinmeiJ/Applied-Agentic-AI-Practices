
##add the actual POST /linkedin endpoint, but still use mock logic. This lets you understand the API contract before adding AI.
## Add request and response models
from fastapi import FastAPI

# after adding service layer (services.py)
from .services import LinkedInService
from .models import LinkedInRequest, LinkedInResponse


# Now we have config.py
# from .config import AZURE_OPENAI_CHAT_DEPLOYMENT
from .config import get_settings

app = FastAPI(
    title="LinkedIn Content Automation API",
    description=(
        "AutoGen-style multi-agent microservice "
        "for LinkedIn content generation."
    ),
    version="1.0.0",
)

## create thes service, its like autowire a class as service
service = LinkedInService()

@app.get("/config")
def config_test():
    settings = get_settings()

    return {
        "chat_deployment": settings.azure_openai_chat_deployment,
        "api_version": settings.azure_openai_api_version,
        "litellm_model": settings.litellm_chat_model,
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

#responsibility is:
# 1. Receive the request.
# 2. Call the service.
# 3. Return the response.
@app.post("/linkedin", response_model=LinkedInResponse)
async def generate_linkedin_post(
    request: LinkedInRequest,
) -> LinkedInResponse:
    return await service.generate_post(request)

