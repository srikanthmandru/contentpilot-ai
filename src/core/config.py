import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except Exception:
    st = None


def get_setting(key: str, default: str = "") -> str:
    if os.getenv(key):
        return os.getenv(key)

    if st is not None:
        try:
            return st.secrets.get(key, default)
        except Exception:
            return default

    return default


class Settings:
    OPENAI_API_KEY: str = get_setting("OPENAI_API_KEY")
    TAVILY_API_KEY: str = get_setting("TAVILY_API_KEY")
    MODEL_NAME: str = get_setting("MODEL_NAME", "gpt-4o-mini")
    ENABLE_IMAGE_GENERATION: bool = (
        str(get_setting("ENABLE_IMAGE_GENERATION", "false")).lower() == "true"
    )

    MEMORY_SUMMARY_TRIGGER: int = 8
    MAX_RECENT_MESSAGES: int = 6


settings = Settings()
