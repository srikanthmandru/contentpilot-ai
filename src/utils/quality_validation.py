from src.core.state import AgentState
from src.integrations.llm_client import get_llm


def quality_validation_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0)

    content_parts = []

    if state.get("blog_output"):
        content_parts.append(f"Blog:\n{state['blog_output']}")

    if state.get("linkedin_output"):
        content_parts.append(f"LinkedIn:\n{state['linkedin_output']}")

    if state.get("image_output"):
        content_parts.append(f"Image Prompt:\n{state['image_output']}")

    if state.get("strategist_output"):
        content_parts.append(f"Strategy:\n{state['strategist_output']}")

    if not content_parts:
        return {
            **state,
            "quality_report": "No generated content available for quality validation.",
        }

    content = "\n\n---\n\n".join(content_parts)
    research = state.get("research_output", "")

    prompt = f"""
You are a content quality validator.

Review the generated marketing content.

Research context:
{research}

Generated content:
{content}

Return a concise quality report with:

1. Overall score out of 10
2. SEO score out of 10, if blog exists
3. LinkedIn engagement score out of 10, if LinkedIn post exists
4. Clarity score out of 10
5. Brand voice consistency score out of 10
6. Hallucination risk: Low / Medium / High
7. Top 3 improvement suggestions
8. Final approval: Approved / Needs Revision

Rules:
- Be strict but practical.
- Flag unsupported claims.
- Prefer clear, useful, non-generic content.
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "quality_report": result.content,
    }
