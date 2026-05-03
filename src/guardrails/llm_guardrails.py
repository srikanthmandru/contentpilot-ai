import json
from src.core.state import AgentState
from src.integrations.llm_client import get_llm

BLOCKED_KEYWORDS = [
    "create fake news",
    "plagiarize",
    "impersonate",
    "misinformation",
    "illegal",
]


def keyword_guardrail(query: str):
    query_lower = query.lower()

    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return False, f"Blocked keyword detected: {keyword}"

    return True, "Keyword check passed."


def llm_safety_check(query: str):
    llm = get_llm(temperature=0)

    prompt = f"""
You are a safety guardrail for an AI content marketing assistant.

Classify the user request.

User request:
{query}

Return ONLY valid JSON:
{{
  "allowed": true,
  "risk": "low",
  "reason": "brief reason"
}}

Block requests involving:
- Fake news
- Impersonation
- Plagiarism
- Deceptive marketing
- Illegal activity
- Harmful misinformation
- Sensitive personal data misuse
- Hate, harassment, or abusive persuasion

Allowed requests:
- Normal marketing content
- SEO writing
- LinkedIn posts
- Research summaries
- Image prompt generation
- Brand strategy
"""

    try:
        result = llm.invoke(prompt)
        parsed = json.loads(result.content)

        return {
            "allowed": bool(parsed.get("allowed", True)),
            "risk": parsed.get("risk", "unknown"),
            "reason": parsed.get("reason", "No reason provided."),
        }

    except Exception:
        return {
            "allowed": True,
            "risk": "unknown",
            "reason": "LLM safety check failed, keyword check will be used.",
        }


def input_guardrail(state: AgentState) -> AgentState:
    query = state.get("user_query", "")

    keyword_allowed, keyword_reason = keyword_guardrail(query)

    if not keyword_allowed:
        return {
            **state,
            "guardrail_status": "blocked",
            "guardrail_notes": [keyword_reason],
            "safety_risk": "high",
            "safety_reason": keyword_reason,
            "final_response": "I can’t help with unsafe, deceptive, or harmful content requests.",
        }

    safety = llm_safety_check(query)

    if not safety["allowed"]:
        return {
            **state,
            "guardrail_status": "blocked",
            "guardrail_notes": [safety["reason"]],
            "safety_risk": safety["risk"],
            "safety_reason": safety["reason"],
            "final_response": "I can’t help with unsafe, deceptive, or harmful content requests.",
        }

    return {
        **state,
        "guardrail_status": "passed",
        "guardrail_notes": [keyword_reason, safety["reason"]],
        "safety_risk": safety["risk"],
        "safety_reason": safety["reason"],
    }


def output_guardrail(state: AgentState) -> AgentState:
    response = state.get("final_response", "")

    if not response.strip():
        return {
            **state,
            "final_response": "I could not generate a valid response. Please try again with more details.",
        }

    risky_phrases = [
        "guaranteed results",
        "100% proven",
        "secret cure",
        "no risk",
    ]

    found = [phrase for phrase in risky_phrases if phrase in response.lower()]

    if found:
        warning = (
            "\n\n---\n\n"
            "## Guardrail Warning\n\n"
            f"Potentially risky marketing claims detected: {', '.join(found)}. "
            "Please verify these claims before publishing."
        )

        return {
            **state,
            "final_response": response + warning,
            "guardrail_notes": state.get("guardrail_notes", [])
            + [f"Output warning for risky phrases: {found}"],
        }

    return state
