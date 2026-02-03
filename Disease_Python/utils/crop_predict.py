import json
import numpy as np
from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_image

# =========================================
# PATHS
# =========================================
MODEL_PATH = "models/crop_classifier.h5"
LABEL_PATH = "labels/crop_labels.json"

# =========================================
# CACHE
# =========================================
MODEL_CACHE = {}

# =========================================
# SUPPORTED CROPS
# =========================================
SUPPORTED_CROPS = ["tomato", "potato", "pepper", "rice", "sugarcane"]

def predict_crop(image_bytes):
    """
    Returns:
    crop name (tomato / potato / pepper / rice / sugarcane / unknown)
    confidence percentage

    image_bytes: bytes from file.read()
    """

    try:
        # Load model (cached)
        if MODEL_PATH not in MODEL_CACHE:
            MODEL_CACHE[MODEL_PATH] = load_model(MODEL_PATH)

        model = MODEL_CACHE[MODEL_PATH]

        # Load labels and threshold
        with open(LABEL_PATH, "r") as f:
            label_data = json.load(f)

        labels = label_data["labels"]
        threshold = label_data.get("confidence_threshold", 0.3)

    except Exception as e:
        print("❌ Crop model error:", e)
        return "unknown", 0.0

    # ✅ Preprocess image from MEMORY
    img = preprocess_image(image_bytes)

    # Predict
    preds = model.predict(img, verbose=0)[0]
    top1 = float(np.max(preds))
    confidence = round(top1 * 100, 2)

    class_index = int(np.argmax(preds))
    crop = labels.get(str(class_index), "unknown").lower()

    # Reject low confidence
    if top1 < threshold:
        return "unknown", confidence

    # Reject unsupported crops
    if crop not in SUPPORTED_CROPS:
        return "unknown", confidence

    return crop, confidence
