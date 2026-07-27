from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient

from .config import get_settings

USE_OLLAMA = True  # True = local Ollama (no cost), False = Azure OpenAI


def create_model_client():
    """
    Create a reusable model client — either local Ollama
    or Azure OpenAI, depending on USE_OLLAMA.
    """

    if USE_OLLAMA:
        return OllamaChatCompletionClient(
            model="deepseek-r1:14b",     # <-- matches your `ollama list` output exactly
            host="http://localhost:11434",
        )

    # --- Azure OpenAI path (disabled while USE_OLLAMA = True) ---
    # settings = get_settings()

    # return AzureOpenAIChatCompletionClient(
    #     azure_deployment=settings.azure_openai_chat_deployment,
    #     model="gpt-5-mini",
    #     api_version=settings.azure_openai_api_version,
    #     azure_endpoint=settings.azure_openai_endpoint,
    #     api_key=settings.azure_openai_api_key,
    # )

