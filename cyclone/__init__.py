from operator import truediv

import openai as ai
from PIL import Image
import os

__api_name__ = ai.__name__
__api_version__ = ai.__version__

def get_api_info():
    return {"name": __api_name__, "version": __api_version__}

def verify_image_file(filepath):
    if not os.path.isfile(filepath):
        return False
    try:
        img = Image.open(filepath)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

# === START OF PACKAGE

__version__ = "0.1.0"
__name__ = "cyclone"

# need to process images and reject invalid formats
# determine which visual fidelity we want the API to operate with
# test which fidelity maintains accuracy without costing too much



def get_package_info():
    return {"name": __name__, "version": __version__}

