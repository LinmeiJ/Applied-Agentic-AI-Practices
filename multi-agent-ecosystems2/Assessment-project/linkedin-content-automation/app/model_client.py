from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from .config import get_settings
from app.enums import ModelType



def create_model_client( model_type: ModelType = ModelType.LOCAL, ):
    if model_type == ModelType.LOCAL:
        return create_local_model_client()
    
    if model_type == ModelType.CLOUD:
        return create_openai_model_client()
    
    # if model_type == ModelType.OPENAI:
    #     return create_claude_model_client()

    raise ValueError(f"Unsupported model type: {model_type}")

    

def create_local_model_client():
    return OllamaChatCompletionClient(
        model="qwen3:8b",     # <-- matches your `ollama list` output exactly
        host="http://localhost:11434",
    )

def create_openai_model_client():
    settings = get_settings()

    return AzureOpenAIChatCompletionClient(
        azure_deployment=settings.azure_openai_chat_deployment,
        model="gpt-5-mini",
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        model_info={ #By explicitly providing model_info, we bypass AutoGen's internal lookup and tell it directly what the model can do
            "vision": False, # Can it process images? No for GPT-4o-mini
            "function_calling": True, # # Can it call functions? Yes
            "json_output": True,       # Can it output JSON mode? Yes
            "structured_output": True, # Can it output structured data? Yes
            "family": "unknown",       # Model family (GPT-4, GPT-3.5, etc.) 
        },
    )