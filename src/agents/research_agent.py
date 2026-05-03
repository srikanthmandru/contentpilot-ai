from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.integrations.search_client import tavily_search


def format_sources(search_results: dict) -> str:
    results = search_results.get("results", [])

    if not results:
        return "No sources found."

    formatted = []

    for index, item in enumerate(results, start=1):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        content = item.get("content", "")

        formatted.append(f"""
Source {index}
Title: {title}
URL: {url}
Summary: {content}
""")

    return "\n".join(formatted)


def research_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.2)
    topic = state.get("topic", state.get("user_query", ""))

    try:
        search_results = tavily_search(topic, max_results=5)
        sources_text = format_sources(search_results)
        quick_answer = search_results.get("answer", "")

        prompt = f"""
You are a deep research agent for a content marketing assistant.

Topic:
{topic}

Search engine quick answer:
{quick_answer}

Sources:
{sources_text}

Create a concise research brief.

Return:
1. Executive summary
2. Key trends
3. Audience pain points
4. Content angles
5. Recommended keywords
6. Source list with title and URL

Rules:
- Use only the provided sources.
- Do not invent facts.
- Clearly mention if source evidence is limited.
- Keep the output useful for content creation.
"""

        result = llm.invoke(prompt)

        return {
            **state,
            "research_output": result.content,
            "research_sources": search_results.get("results", []),
        }

    except Exception as e:
        fallback_prompt = f"""
You are a research assistant.

The web search failed, so create a lightweight research plan for:
{topic}

Return:
- What to research
- Search queries to use
- Likely audience pain points
- Possible content angles

Clearly mention that live web research failed.
"""

        result = llm.invoke(fallback_prompt)

        return {
            **state,
            "research_output": result.content,
            "research_sources": [],
            "errors": state.get("errors", []) + [f"Research search error: {str(e)}"],
        }
