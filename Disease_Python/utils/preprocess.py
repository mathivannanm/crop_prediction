import cv2
import numpy as np

IMG_SIZE = (224, 224)

def preprocess_image(image_bytes):
    """
    Preprocess image directly from memory (no file save).
    image_bytes: bytes from file.read()
    """

    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image data")

    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize
    img = cv2.resize(img, IMG_SIZE)

    # Normalize
    img = img / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    return img
