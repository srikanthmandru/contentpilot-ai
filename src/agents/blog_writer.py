from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.core.brand_voice import format_brand_voice
from src.core.content_templates import format_template_settings


def blog_writer_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.4)

    topic = state.get("topic", "")
    research = state.get("research_output", "")
    brand_voice = format_brand_voice(state.get("brand_voice"))
    template_settings = format_template_settings(state.get("template_settings"))

    prompt = f"""
You are an SEO blog writer.

Create an SEO-optimized blog for:
{topic}

Use this research:
{research}

Brand voice guidelines:
{brand_voice}

Content template settings:
{template_settings}

Return:
- SEO title
- Meta description under 160 characters
- Suggested keywords
- Blog outline
- Full blog draft
- CTA

Make it useful, specific, and non-generic.
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "blog_output": result.content,
    }
