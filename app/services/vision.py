import base64, io
from PIL import Image

def classify_topk(image_b64: str, k: int = 3):
    # Validate input decodes; real TF model can be added later
    Image.open(io.BytesIO(base64.b64decode(image_b64)))
    return [("grilled chicken", 0.72), ("salad", 0.18), ("rice", 0.10)]