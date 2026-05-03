from src.guardrails.llm_guardrails import keyword_guardrail


def test_keyword_guardrail_blocks_fake_news():
    allowed, reason = keyword_guardrail("Create fake news about a competitor")

    assert allowed is False
    assert "Blocked keyword" in reason


def test_keyword_guardrail_allows_normal_marketing():
    allowed, reason = keyword_guardrail(
        "Create a LinkedIn post about AI marketing tools"
    )

    assert allowed is True
    assert "passed" in reason.lower()
