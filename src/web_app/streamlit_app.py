import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from src.core.workflow import (
    run_workflow,
    regenerate_blog,
    regenerate_linkedin,
    regenerate_image_prompt,
    regenerate_strategy,
    improve_quality,
)
from src.core.content_templates import (
    BLOG_TEMPLATES,
    LINKEDIN_TEMPLATES,
    STRATEGY_TEMPLATES,
)
from src.utils.export_tools import build_export_content

st.set_page_config(
    page_title="ContentPilot AI",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ ContentPilot AI")
st.caption("Multi-Agent AI Content Marketing Assistant")


# -----------------------------
# Session State
# -----------------------------
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "messages": [],
        "memory_summary": "",
        "errors": [],
        "brand_voice": {},
        "template_settings": {},
    }


# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.title("Settings")

st.sidebar.subheader("Brand Voice Settings")

existing_brand_voice = st.session_state.agent_state.get("brand_voice", {})

audience = st.sidebar.text_input(
    "Audience",
    value=existing_brand_voice.get("audience", "startup founders and marketing teams"),
)

tone = st.sidebar.text_input(
    "Tone",
    value=existing_brand_voice.get("tone", "clear, practical, professional"),
)

style = st.sidebar.text_input(
    "Style",
    value=existing_brand_voice.get("style", "concise, human, non-generic"),
)

reading_level = st.sidebar.text_input(
    "Reading Level",
    value=existing_brand_voice.get("reading_level", "easy to understand"),
)

avoid = st.sidebar.text_input(
    "Avoid",
    value=existing_brand_voice.get("avoid", "jargon, hype, unsupported claims"),
)

brand_voice = {
    "audience": audience,
    "tone": tone,
    "style": style,
    "reading_level": reading_level,
    "avoid": avoid,
}

st.session_state.agent_state["brand_voice"] = brand_voice


st.sidebar.subheader("Content Templates")

existing_templates = st.session_state.agent_state.get("template_settings", {})

blog_template = st.sidebar.selectbox(
    "Blog Template",
    options=list(BLOG_TEMPLATES.keys()),
    index=(
        list(BLOG_TEMPLATES.keys()).index(
            existing_templates.get("blog_template", "Auto")
        )
        if existing_templates.get("blog_template", "Auto") in BLOG_TEMPLATES
        else 0
    ),
)

linkedin_template = st.sidebar.selectbox(
    "LinkedIn Template",
    options=list(LINKEDIN_TEMPLATES.keys()),
    index=(
        list(LINKEDIN_TEMPLATES.keys()).index(
            existing_templates.get("linkedin_template", "Auto")
        )
        if existing_templates.get("linkedin_template", "Auto") in LINKEDIN_TEMPLATES
        else 0
    ),
)

strategy_template = st.sidebar.selectbox(
    "Strategy Template",
    options=list(STRATEGY_TEMPLATES.keys()),
    index=(
        list(STRATEGY_TEMPLATES.keys()).index(
            existing_templates.get("strategy_template", "Auto")
        )
        if existing_templates.get("strategy_template", "Auto") in STRATEGY_TEMPLATES
        else 0
    ),
)

template_settings = {
    "blog_template": blog_template,
    "linkedin_template": linkedin_template,
    "strategy_template": strategy_template,
}

st.session_state.agent_state["template_settings"] = template_settings


# -----------------------------
# Chat History
# -----------------------------
for message in st.session_state.agent_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# Chat Input + Workflow
# -----------------------------
user_query = st.chat_input(
    "Ask me to research, write a blog, create a LinkedIn post, or generate image ideas..."
)

if user_query:
    with st.chat_message("user"):
        st.write(user_query)

    with st.spinner("Thinking..."):
        result = run_workflow(
            user_query=user_query,
            existing_state=st.session_state.agent_state,
            brand_voice=brand_voice,
            template_settings=template_settings,
        )

        st.session_state.agent_state = result

    with st.chat_message("assistant"):
        st.write(result.get("final_response", "No response generated."))


# -----------------------------
# Content Existence Check
# -----------------------------
has_content = any(
    [
        st.session_state.agent_state.get("research_output"),
        st.session_state.agent_state.get("blog_output"),
        st.session_state.agent_state.get("linkedin_output"),
        st.session_state.agent_state.get("image_output"),
        st.session_state.agent_state.get("strategist_output"),
        st.session_state.agent_state.get("quality_report"),
    ]
)


# -----------------------------
# Content Dashboard
# -----------------------------
if has_content:
    st.divider()
    st.subheader("Content Dashboard")

    tabs = st.tabs(
        [
            "Research",
            "Blog",
            "LinkedIn",
            "Image Prompt",
            "Strategy",
            "Quality",
        ]
    )

    with tabs[0]:
        st.text_area(
            "Research Output",
            value=st.session_state.agent_state.get("research_output", ""),
            height=300,
            key="edited_research",
        )

    with tabs[1]:
        st.text_area(
            "Blog Output",
            value=st.session_state.agent_state.get("blog_output", ""),
            height=500,
            key="edited_blog",
        )

    with tabs[2]:
        st.text_area(
            "LinkedIn Output",
            value=st.session_state.agent_state.get("linkedin_output", ""),
            height=350,
            key="edited_linkedin",
        )

    with tabs[3]:
        st.text_area(
            "Image Prompt Output",
            value=st.session_state.agent_state.get("image_output", ""),
            height=350,
            key="edited_image",
        )

        image_path = st.session_state.agent_state.get("generated_image_path")

        if image_path:
            st.image(image_path, caption="Generated Image")

    with tabs[4]:
        st.text_area(
            "Strategy Output",
            value=st.session_state.agent_state.get("strategist_output", ""),
            height=400,
            key="edited_strategy",
        )

    with tabs[5]:
        st.text_area(
            "Quality Report",
            value=st.session_state.agent_state.get("quality_report", ""),
            height=300,
            key="edited_quality",
        )

    if st.button("Save Edits"):
        st.session_state.agent_state["research_output"] = st.session_state.get(
            "edited_research", ""
        )
        st.session_state.agent_state["blog_output"] = st.session_state.get(
            "edited_blog", ""
        )
        st.session_state.agent_state["linkedin_output"] = st.session_state.get(
            "edited_linkedin", ""
        )
        st.session_state.agent_state["image_output"] = st.session_state.get(
            "edited_image", ""
        )
        st.session_state.agent_state["strategist_output"] = st.session_state.get(
            "edited_strategy", ""
        )
        st.session_state.agent_state["quality_report"] = st.session_state.get(
            "edited_quality", ""
        )

        st.success("Edits saved.")

    # -----------------------------
    # Regeneration Controls
    # -----------------------------
    st.divider()
    st.subheader("Regenerate Sections")

    refinement_instruction = st.text_input(
        "Optional refinement instruction",
        key="refinement_instruction",
        placeholder="Example: Make it shorter, more founder-friendly, or more technical...",
    )

    if refinement_instruction:
        st.session_state.agent_state["refinement_instruction"] = refinement_instruction

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Regenerate Blog"):
            with st.spinner("Regenerating blog..."):
                st.session_state.agent_state = regenerate_blog(
                    st.session_state.agent_state
                )
            st.success("Blog regenerated.")
            st.rerun()

    with col2:
        if st.button("Regenerate LinkedIn"):
            with st.spinner("Regenerating LinkedIn post..."):
                st.session_state.agent_state = regenerate_linkedin(
                    st.session_state.agent_state
                )
            st.success("LinkedIn post regenerated.")
            st.rerun()

    with col3:
        if st.button("Regenerate Image Prompt"):
            with st.spinner("Regenerating image prompt..."):
                st.session_state.agent_state = regenerate_image_prompt(
                    st.session_state.agent_state
                )
            st.success("Image prompt regenerated.")
            st.rerun()

    with col4:
        if st.button("Regenerate Strategy"):
            with st.spinner("Regenerating strategy..."):
                st.session_state.agent_state = regenerate_strategy(
                    st.session_state.agent_state
                )
            st.success("Strategy regenerated.")
            st.rerun()

    with col5:
        if st.button("Improve Quality"):
            with st.spinner("Updating quality report..."):
                st.session_state.agent_state = improve_quality(
                    st.session_state.agent_state
                )
            st.success("Quality report updated.")
            st.rerun()

    # -----------------------------
    # Downloads
    # -----------------------------
    st.divider()
    st.subheader("Download Generated Content")

    export_content = build_export_content(st.session_state.agent_state)

    st.download_button(
        label="Download Markdown",
        data=export_content,
        file_name="contentpilot_output.md",
        mime="text/markdown",
    )

    st.download_button(
        label="Download Text",
        data=export_content,
        file_name="contentpilot_output.txt",
        mime="text/plain",
    )

    st.download_button(
        label="Download HTML",
        data=f"<pre>{export_content}</pre>",
        file_name="contentpilot_output.html",
        mime="text/html",
    )


# -----------------------------
# Sidebar Debug Info
# -----------------------------
st.sidebar.divider()
st.sidebar.subheader("Detected Intents")
st.sidebar.write(st.session_state.agent_state.get("intents", []))

st.sidebar.subheader("Topic")
st.sidebar.write(st.session_state.agent_state.get("topic", ""))

st.sidebar.subheader("Guardrail Status")
st.sidebar.write(st.session_state.agent_state.get("guardrail_status", ""))

st.sidebar.subheader("Safety Risk")
st.sidebar.write(st.session_state.agent_state.get("safety_risk", "N/A"))

st.sidebar.subheader("Safety Reason")
st.sidebar.write(st.session_state.agent_state.get("safety_reason", "N/A"))

st.sidebar.subheader("Memory Summary")
st.sidebar.write(st.session_state.agent_state.get("memory_summary", "No summary yet."))

st.sidebar.subheader("Research Sources")
sources = st.session_state.agent_state.get("research_sources", [])

if sources:
    for source in sources:
        title = source.get("title", "Untitled")
        url = source.get("url", "")
        st.sidebar.markdown(f"- [{title}]({url})")
else:
    st.sidebar.write("No sources yet.")

if st.session_state.agent_state.get("errors"):
    st.sidebar.subheader("Errors")
    st.sidebar.write(st.session_state.agent_state.get("errors"))
