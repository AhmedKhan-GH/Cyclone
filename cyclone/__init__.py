import openai as ai
from PIL import Image, UnidentifiedImageError
import logging
import os
from pydantic import BaseModel, Field
from typing import Optional

__version__ = "0.1.0"
logger = logging.getLogger(__name__)

def get_api_key():
    try:
        return os.environ['OPENAI_API_KEY']
    except KeyError as e:
        logger.error(f"missing environment variable {e}")
        return None

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

from typing import Optional

class ObjectClass(BaseModel):
    object: str = Field(description="specific name for what the object is")                   # What the object is (e.g., "Laptop", "Sofa")
    condition: str = Field(description="state of wear between new, like new, used, or damaged")                # e.g., "new", "used - like new", "damaged"
    category: str = Field(description="generic category regarding what the object is for")    # Broad category (e.g., "electronics", "furniture")s
    brand: Optional[str] = Field(description="the brand name if easily visible from labeling")  # Brand name if known
    style: Optional[str] = Field(description="characteristic of aesthetic or utility based on object")


# have a way to reject images that are too large at this level
# the front end team will also have restrictions on file upload
# but this needs to be a last line of defense to not overuse tokens

def classify_image(
        filepath: str,
        model: str = "gpt-5-nano",
        schema: type[BaseModel] = ObjectClass
) -> dict | None:
    if not get_api_key():
        return None
    client = ai.OpenAI()
    info = get_image_info(filepath)
    if info not in ("PNG", "WEBP", "JPEG", "GIF"):
        logging.error(f"invalid image format: {info}")
        return None
    response = client.responses.parse(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "extract precise image information and output short lowercase responses"},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "identify aspects of only the most prominent object in the image"},
                    {"type": "input_image", "file_id": create_file(filepath)}
                ]
            }
        ],
        text_format=ObjectClass,
    )

    # have more logging around transient API failures because they can be for a whole
    # host of reasons, openAI always has outages, the user should be informed so need
    # robust error raising and logging

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
    if not get_api_key():
        return None
    client = ai.OpenAI()
    with open(file_path, "rb") as file_content:
        result = client.files.create(
            file=file_content,
            purpose="vision",
        )
    return result.id

def get_package_info():
    return {"name": __name__, "version": __version__}
