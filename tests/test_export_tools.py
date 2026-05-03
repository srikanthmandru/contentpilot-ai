from src.utils.export_tools import slugify, build_export_content


def test_slugify():
    assert slugify("AI Marketing Tools!") == "ai-marketing-tools"


def test_build_export_content():
    state = {
        "research_output": "Research here",
        "blog_output": "Blog here",
        "linkedin_output": "LinkedIn here",
    }

    output = build_export_content(state)

    assert "Research here" in output
    assert "Blog here" in output
    assert "LinkedIn here" in output
