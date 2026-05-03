from tavily import TavilyClient
from src.core.config import settings


def tavily_search(query: str, max_results: int = 5):
    if not settings.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing. Add it to your .env file.")

    client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=True,
        include_raw_content=False,
    )

    return response
