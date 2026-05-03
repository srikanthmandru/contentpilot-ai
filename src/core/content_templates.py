BLOG_TEMPLATES = {
    "Auto": "Choose the best blog format for the user request.",
    "How-To Guide": "Step-by-step educational blog with practical actions.",
    "Listicle": "Numbered list blog with clear takeaways.",
    "Comparison": "Compare options, pros, cons, and recommendations.",
    "Thought Leadership": "Insightful POV article with trends and expert framing.",
}

LINKEDIN_TEMPLATES = {
    "Auto": "Choose the best LinkedIn format for the user request.",
    "Industry Insight": "Professional insight post with trend analysis.",
    "Practical Tips": "Actionable tips post with short, scannable points.",
    "Story Post": "Narrative-style post with lesson learned.",
    "Question-Led Post": "Starts with a strong question to drive engagement.",
}

STRATEGY_TEMPLATES = {
    "Auto": "Choose the best strategy format for the user request.",
    "Weekly Plan": "7-day content plan with topics and channels.",
    "Campaign Plan": "Campaign goal, audience, themes, channels, and schedule.",
    "Content Pillars": "Core themes, messaging angles, and repeatable ideas.",
    "Launch Plan": "Pre-launch, launch, and post-launch content strategy.",
}


def format_template_settings(template_settings: dict | None) -> str:
    settings = template_settings or {}

    return f"""
Blog template: {settings.get("blog_template", "Auto")}
Blog template guidance: {BLOG_TEMPLATES.get(settings.get("blog_template", "Auto"))}

LinkedIn template: {settings.get("linkedin_template", "Auto")}
LinkedIn template guidance: {LINKEDIN_TEMPLATES.get(settings.get("linkedin_template", "Auto"))}

Strategy template: {settings.get("strategy_template", "Auto")}
Strategy template guidance: {STRATEGY_TEMPLATES.get(settings.get("strategy_template", "Auto"))}
"""
