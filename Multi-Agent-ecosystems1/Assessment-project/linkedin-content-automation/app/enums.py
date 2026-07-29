from enum import Enum

class ModelType(str, Enum):
    LOCAL = "local" #ollama
    ANTROPIC = "Claude"
    OPENAI = "openai" #via Azure