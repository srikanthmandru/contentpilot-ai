import json
from pydantic import BaseModel, Field, ValidationError
from typing import List

from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.memory.conversation_memory import get_recent_context

VALID_INTENTS = ["research", "blog", "linkedin", "image", "strategy"]


class RouterDecision(BaseModel):
    intents: List[str] = Field(default_factory=list)
    topic: str


def normalize_intents(intents: List[str]) -> List[str]:
    clean_intents = []

    for intent in intents:
        intent = intent.lower().strip()
        if intent in VALID_INTENTS and intent not in clean_intents:
            clean_intents.append(intent)

    return clean_intents or ["research"]


def safe_json_parse(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            return json.loads(text[start:end])

        raise


def query_handler_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0)

    query = state.get("user_query", "")
    context = get_recent_context(state)

    prompt = f"""
You are a query routing agent for an AI Content Marketing Assistant.

Detect all user intents from this exact list:
{VALID_INTENTS}

Return multiple intents for multi-intent requests.

Intent rules:
- research: research, analyze, compare, find trends, gather sources
- blog: article, SEO post, long-form content, blog
- linkedin: LinkedIn post, professional social post
- image: image, visual, banner, creative, design prompt
- strategy: content plan, campaign, calendar, positioning, messaging

Return ONLY valid JSON:
{{
  "intents": ["research", "blog"],
  "topic": "clear topic here"
}}

Conversation context:
{context}

User query:
{query}
"""

    try:
        result = llm.invoke(prompt)
        parsed = safe_json_parse(result.content)

        decision = RouterDecision(**parsed)

        intents = normalize_intents(decision.intents)
        topic = decision.topic.strip() or query

        return {
            **state,
            "intents": intents,
            "topic": topic,
        }

    except (ValidationError, Exception) as e:
        return {
            **state,
            "intents": ["research"],
            "topic": query,
            "errors": state.get("errors", [])
            + [f"Query handler validation error: {str(e)}"],
        }
