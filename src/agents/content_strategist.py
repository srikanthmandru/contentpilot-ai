from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.core.brand_voice import format_brand_voice
from src.core.content_templates import format_template_settings


def content_strategist_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.3)

    topic = state.get("topic", "")
    research = state.get("research_output", "")
    brand_voice = format_brand_voice(state.get("brand_voice"))
    template_settings = format_template_settings(state.get("template_settings"))

    prompt = f"""
You are a content marketing strategist.

Create a content strategy for:
{topic}

Use this research:
{research}

Brand voice guidelines:
{brand_voice}

Content template settings:
{template_settings}

Return:
- Target audience
- Content goals
- Key messaging
- Recommended channels
- 5 content ideas
- Weekly content plan

Keep it practical and execution-focused.
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "strategist_output": result.content,
    }
