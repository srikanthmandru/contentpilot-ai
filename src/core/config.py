import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    ENABLE_IMAGE_GENERATION: bool = (
        os.getenv("ENABLE_IMAGE_GENERATION", "false").lower() == "true"
    )

    MEMORY_SUMMARY_TRIGGER: int = 8
    MAX_RECENT_MESSAGES: int = 6


settings = Settings()
