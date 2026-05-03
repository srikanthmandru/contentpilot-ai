from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.core.brand_voice import format_brand_voice
from src.core.content_templates import format_template_settings


def linkedin_writer_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.5)

    topic = state.get("topic", "")
    research = state.get("research_output", "")
    brand_voice = format_brand_voice(state.get("brand_voice"))
    template_settings = format_template_settings(state.get("template_settings"))

    prompt = f"""
You are a LinkedIn content strategist.

Create a LinkedIn post for:
{topic}

Use this research:
{research}

Brand voice guidelines:
{brand_voice}

Content template settings:
{template_settings}

Return:
- Strong opening hook
- LinkedIn post body
- CTA question
- 8-12 hashtags

Keep it professional, human, and easy to read.
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "linkedin_output": result.content,
    }
