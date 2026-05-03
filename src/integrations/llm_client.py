from langchain_openai import ChatOpenAI
from src.core.config import settings


def get_llm(temperature: float = 0.2):
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    return ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )
