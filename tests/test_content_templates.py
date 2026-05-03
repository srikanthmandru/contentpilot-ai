from src.core.content_templates import format_template_settings


def test_format_template_settings():
    settings = {
        "blog_template": "How-To Guide",
        "linkedin_template": "Practical Tips",
        "strategy_template": "Weekly Plan",
    }

    output = format_template_settings(settings)

    assert "How-To Guide" in output
    assert "Practical Tips" in output
    assert "Weekly Plan" in output
