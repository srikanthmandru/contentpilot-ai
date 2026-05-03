from pathlib import Path
from datetime import datetime
import re

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60] or "content"


def build_export_content(state: dict) -> str:
    sections = []

    if state.get("research_output"):
        sections.append(f"# Research Summary\n\n{state['research_output']}")

    if state.get("blog_output"):
        sections.append(f"# SEO Blog Draft\n\n{state['blog_output']}")

    if state.get("linkedin_output"):
        sections.append(f"# LinkedIn Post\n\n{state['linkedin_output']}")

    if state.get("image_output"):
        sections.append(f"# Image Prompt\n\n{state['image_output']}")

    if state.get("strategist_output"):
        sections.append(f"# Content Strategy\n\n{state['strategist_output']}")

    if state.get("quality_report"):
        sections.append(f"# Quality Report\n\n{state['quality_report']}")

    return "\n\n---\n\n".join(sections)


def save_markdown(state: dict) -> Path:
    topic = slugify(state.get("topic", "content"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"{topic}_{timestamp}.md"

    file_path.write_text(build_export_content(state), encoding="utf-8")
    return file_path


def save_text(state: dict) -> Path:
    topic = slugify(state.get("topic", "content"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"{topic}_{timestamp}.txt"

    file_path.write_text(build_export_content(state), encoding="utf-8")
    return file_path


def save_html(state: dict) -> Path:
    topic = slugify(state.get("topic", "content"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"{topic}_{timestamp}.html"

    content = build_export_content(state)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{state.get("topic", "Content Export")}</title>
</head>
<body>
    <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">
{content}
    </pre>
</body>
</html>
"""

    file_path.write_text(html, encoding="utf-8")
    return file_path
