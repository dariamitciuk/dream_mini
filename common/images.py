import os
import requests


IMAGE_CAPTIONING_SERVICE_URL = os.getenv("IMAGE_CAPTIONING_SERVICE_URL", "http://0.0.0.0:8123/respond")


def get_caption(texts, timeout=1):
    result = requests.post(IMAGE_CAPTIONING_SERVICE_URL, json={"texts": texts}, timeout=timeout).json()["caption"] # texts?
    return result

IMAGE_PATTERN =[] # ask