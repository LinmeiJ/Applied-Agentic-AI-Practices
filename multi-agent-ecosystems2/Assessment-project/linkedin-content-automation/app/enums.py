from enum import Enum

class ModelType(str, Enum):
    LOCAL = "local" #ollama
    CLOUD = "cloud"