from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    user_query: str
    conversation_id: str

    intents: List[str]
    topic: str

    messages: List[Dict[str, str]]
    memory_summary: str

    research_output: Optional[str]
    research_sources: List[Dict[str, Any]]

    blog_output: Optional[str]
    linkedin_output: Optional[str]
    image_output: Optional[str]
    strategist_output: Optional[str]
    quality_report: Optional[str]

    guardrail_status: str
    guardrail_notes: List[str]
    safety_risk: Optional[str]
    safety_reason: Optional[str]

    brand_voice: Dict[str, Any]
    template_settings: Dict[str, Any]
    generated_image_path: Optional[str]

    final_response: str
    errors: List[str]
