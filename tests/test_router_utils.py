from src.agents.query_handler import normalize_intents, safe_json_parse


def test_normalize_intents():
    result = normalize_intents(["blog", "linkedin", "blog", "unknown"])

    assert result == ["blog", "linkedin"]


def test_normalize_intents_defaults_to_research():
    result = normalize_intents(["unknown"])

    assert result == ["research"]


def test_safe_json_parse():
    text = """
    Here is the JSON:
    {"intents": ["blog"], "topic": "AI marketing"}
    """

    result = safe_json_parse(text)

    assert result["intents"] == ["blog"]
    assert result["topic"] == "AI marketing"
