import openai as ai
from PIL import Image, UnidentifiedImageError
import logging
import os
from pydantic import BaseModel
from typing import Optional

# tasks, perhaps have pydantic schemas be passed in rather
# than hard coded in the utility, this will enable back
# end engineers determine what aspects they want to extract

__version__ = "0.1.0"
logger = logging.getLogger(__name__)

def get_api_key():
    try:
        return os.environ['OPENAI_API_KEY']
    except KeyError as e:
        logger.error(f"missing environment variable {e}")
        raise

def get_api_info():
    return {"name": ai.__name__, "version": ai.__version__}

def get_image_info(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()
        with Image.open(filepath) as img:
            return img.format
    except UnidentifiedImageError as e:
        logger.warning(f"{e}")
        return None
    except OSError as e:
        logger.warning(f"operating system error: {e}")
        return None

client = ai.OpenAI()

from typing import Optional

class ObjectClass(BaseModel):
    name: str                    # What the object is (e.g., "Laptop", "Sofa")
    brand: Optional[str] = None  # Brand name if known
    condition: str               # e.g., "new", "used - like new", "damaged"
    category: Optional[str] = None  # Broad category (e.g., "electronics", "furniture")s

def classify_image(
        filepath: str,
        model: str = "gpt-5-nano",
        schema: type[BaseModel] = ObjectClass
) -> dict | None:
    api_key = get_api_key()
    if not get_image_info(filepath):
        return None
    response = client.responses.parse(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "Extract the image information."},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "what's in this image?"},
                    {
                        "type": "input_image",
                        "file_id": create_file(filepath)
                    }
                ]
            }
        ],
        text_format=ObjectClass,
    )

    return next(
    (
        c.parsed.model_dump()
        for item in getattr(response, "output", []) or []
        for c in getattr(item, "content", []) or []
        if isinstance(getattr(c, "parsed", None), BaseModel)
    ),
    None
)

def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

def get_package_info():
    return {"name": __name__, "version": __version__}
