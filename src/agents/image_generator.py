from src.core.state import AgentState
from src.integrations.llm_client import get_llm
from src.integrations.image_client import generate_image
from src.core.brand_voice import format_brand_voice


def image_generator_agent(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.4)

    topic = state.get("topic", "")
    research = state.get("research_output", "")
    brand_voice = format_brand_voice(state.get("brand_voice"))
    refinement = state.get("refinement_instruction", "")

    prompt = f"""
You are an AI image prompt engineer for marketing visuals.

Create an image generation prompt for:
{topic}

Brand voice guidelines:
{brand_voice}

Use this context:
{research}

Refinement instruction:
{refinement}

Return:
- Image concept
- Detailed image prompt
- Style
- Aspect ratio recommendation
- Negative prompt

Make it suitable for professional marketing content.
"""

    result = llm.invoke(prompt)
    image_prompt_output = result.content

    generated_image_path = None
    image_generation_note = ""

    try:
        image_result = generate_image(image_prompt_output)
        generated_image_path = image_result.get("image_path")
        image_generation_note = image_result.get("message", "")
    except Exception as e:
        image_generation_note = (
            f"Image generation failed. Prompt-only mode used. Error: {str(e)}"
        )

    final_image_output = f"""
{image_prompt_output}

---

Image generation status:
{image_generation_note}
"""

    return {
        **state,
        "image_output": final_image_output,
        "generated_image_path": generated_image_path,
    }
