from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from .config import get_settings


def create_model_client() -> AzureOpenAIChatCompletionClient:
    """
    Create a reusable Azure OpenAI client.
    """

    settings = get_settings()

    return AzureOpenAIChatCompletionClient(
        azure_deployment=settings.azure_openai_chat_deployment,
        model="gpt-5-mini",
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )