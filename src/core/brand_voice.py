DEFAULT_BRAND_VOICE = {
    "audience": "startup founders and marketing teams",
    "tone": "clear, practical, professional",
    "style": "concise, human, non-generic",
    "reading_level": "easy to understand",
    "avoid": "jargon, hype, unsupported claims",
}


def format_brand_voice(brand_voice: dict | None) -> str:
    voice = brand_voice or DEFAULT_BRAND_VOICE

    return f"""
Audience: {voice.get("audience")}
Tone: {voice.get("tone")}
Style: {voice.get("style")}
Reading level: {voice.get("reading_level")}
Avoid: {voice.get("avoid")}
"""
