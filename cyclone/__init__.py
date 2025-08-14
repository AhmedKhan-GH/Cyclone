from operator import truediv

import openai as ai
from PIL import Image, UnidentifiedImageError
import logging

def get_api_info():
    return {"name": ai.__name__, "version": ai.__version__}

__version__ = "0.1.0"

def get_package_info():
    return {"name": __name__, "version": __version__}

logger = logging.getLogger(__name__)

def get_image_info(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()
        with Image.open(filepath) as img:
            return img.format
    except (UnidentifiedImageError, OSError) as e:
        # OSError already includes PermissionError, FileNotFoundError
        # UnidentifiedImageError originates from Pillow, all other
        # throw runtime exceptions
        logger.warning(f"{e}")
        return None


# === START OF PACKAGE


# determine which visual fidelity we want the API to operate with
# test which fidelity maintains accuracy without costing too much

