from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str | None = None # not required by this assignment
    tavily_api_key: str | None = None # not required by this assignment

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def litellm_chat_model(self) -> str:
        return f"azure/{self.azure_openai_chat_deployment}"


@lru_cache # It caches the first Settings object and reuses it later.
def get_settings() -> Settings:
    return Settings()
