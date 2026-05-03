from langgraph.graph import StateGraph, END

from src.core.state import AgentState
from src.guardrails.llm_guardrails import input_guardrail, output_guardrail
from src.agents.query_handler import query_handler_agent
from src.agents.research_agent import research_agent
from src.agents.blog_writer import blog_writer_agent
from src.agents.linkedin_writer import linkedin_writer_agent
from src.agents.image_generator import image_generator_agent
from src.agents.content_strategist import content_strategist_agent
from src.memory.conversation_memory import (
    add_user_message,
    add_ai_message,
    summarize_conversation,
)
from src.utils.quality_validation import quality_validation_agent


def blocked_or_continue(state: AgentState):
    if state.get("guardrail_status") == "blocked":
        return "blocked"
    return "continue"


def needs_research(state: AgentState):
    intents = state.get("intents", [])
    if any(
        intent in intents
        for intent in ["research", "blog", "linkedin", "image", "strategy"]
    ):
        return "research"
    return "compose"


def run_blog_if_needed(state: AgentState) -> AgentState:
    if "blog" in state.get("intents", []):
        return blog_writer_agent(state)
    return state


def run_linkedin_if_needed(state: AgentState) -> AgentState:
    if "linkedin" in state.get("intents", []):
        return linkedin_writer_agent(state)
    return state


def run_image_if_needed(state: AgentState) -> AgentState:
    if "image" in state.get("intents", []):
        return image_generator_agent(state)
    return state


def run_strategy_if_needed(state: AgentState) -> AgentState:
    if "strategy" in state.get("intents", []):
        return content_strategist_agent(state)
    return state


def compose_final_response(state: AgentState) -> AgentState:
    sections = []

    if state.get("research_output") and "research" in state.get("intents", []):
        sections.append(f"## Research Summary\n\n{state['research_output']}")

    if state.get("blog_output"):
        sections.append(f"## SEO Blog Draft\n\n{state['blog_output']}")

    if state.get("linkedin_output"):
        sections.append(f"## LinkedIn Post\n\n{state['linkedin_output']}")

    if state.get("image_output"):
        sections.append(f"## Image Prompt\n\n{state['image_output']}")

    if state.get("strategist_output"):
        sections.append(f"## Content Strategy\n\n{state['strategist_output']}")

    if state.get("quality_report"):
        sections.append(f"## Quality Report\n\n{state['quality_report']}")

    final_response = "\n\n---\n\n".join(sections)

    if not final_response:
        final_response = (
            "I understood your request, but no matching content agent was selected."
        )

    updated_state = {
        **state,
        "final_response": final_response,
    }

    updated_state = add_ai_message(updated_state, final_response)
    updated_state = summarize_conversation(updated_state)

    return updated_state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("input_guardrail", input_guardrail)
    graph.add_node("query_handler", query_handler_agent)
    graph.add_node("research_agent", research_agent)
    graph.add_node("blog_agent", run_blog_if_needed)
    graph.add_node("linkedin_agent", run_linkedin_if_needed)
    graph.add_node("image_agent", run_image_if_needed)
    graph.add_node("strategy_agent", run_strategy_if_needed)
    graph.add_node("compose_final_response", compose_final_response)
    graph.add_node("output_guardrail", output_guardrail)
    graph.add_node("quality_validation", quality_validation_agent)

    graph.set_entry_point("input_guardrail")

    graph.add_conditional_edges(
        "input_guardrail",
        blocked_or_continue,
        {
            "blocked": "output_guardrail",
            "continue": "query_handler",
        },
    )

    graph.add_conditional_edges(
        "query_handler",
        needs_research,
        {
            "research": "research_agent",
            "compose": "compose_final_response",
        },
    )

    graph.add_edge("research_agent", "blog_agent")
    graph.add_edge("blog_agent", "linkedin_agent")
    graph.add_edge("linkedin_agent", "image_agent")
    graph.add_edge("image_agent", "strategy_agent")
    graph.add_edge("strategy_agent", "quality_validation")
    graph.add_edge("quality_validation", "compose_final_response")
    graph.add_edge("compose_final_response", "output_guardrail")
    graph.add_edge("output_guardrail", END)

    return graph.compile()


app_graph = build_graph()


def run_workflow(
    user_query: str,
    existing_state: AgentState | None = None,
    brand_voice: dict | None = None,
    template_settings: dict | None = None,
):
    state = existing_state or {
        "messages": [],
        "memory_summary": "",
        "errors": [],
    }

    state = {
        **state,
        "user_query": user_query,
        "brand_voice": brand_voice or state.get("brand_voice", {}),
        "template_settings": template_settings or state.get("template_settings", {}),
    }

    state = add_user_message(state, user_query)

    return app_graph.invoke(state)


def regenerate_blog(existing_state: AgentState):
    state = blog_writer_agent(existing_state)
    state = quality_validation_agent(state)
    return compose_final_response(state)


def regenerate_linkedin(existing_state: AgentState):
    state = linkedin_writer_agent(existing_state)
    state = quality_validation_agent(state)
    return compose_final_response(state)


def regenerate_image_prompt(existing_state: AgentState):
    state = image_generator_agent(existing_state)
    state = quality_validation_agent(state)
    return compose_final_response(state)


def regenerate_strategy(existing_state: AgentState):
    state = content_strategist_agent(existing_state)
    state = quality_validation_agent(state)
    return compose_final_response(state)


def improve_quality(existing_state: AgentState):
    state = quality_validation_agent(existing_state)
    return compose_final_response(state)
