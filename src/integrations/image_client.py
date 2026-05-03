import base64
from pathlib import Path
from datetime import datetime
from openai import OpenAI

from src.core.config import settings

IMAGE_OUTPUT_DIR = Path("outputs/images")
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_image(prompt: str) -> dict:
    if not settings.ENABLE_IMAGE_GENERATION:
        return {
            "enabled": False,
            "image_path": None,
            "message": "Image generation is disabled. Set ENABLE_IMAGE_GENERATION=true to enable it.",
        }

    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = IMAGE_OUTPUT_DIR / f"generated_image_{timestamp}.png"

    image_path.write_bytes(image_bytes)

    return {
        "enabled": True,
        "image_path": str(image_path),
        "message": "Image generated successfully.",
    }
