import json
import numpy as np
from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_image

# =========================================
# CACHE (avoid reloading models)
# =========================================
MODEL_CACHE = {}

def predict_disease(image_bytes, model_path, label_path):
    """
    Predict disease from image bytes (NO file save)

    image_bytes : bytes from file.read()
    model_path  : path to disease model (.h5)
    label_path  : path to label json
    """

    try:
        # Load model (cached)
        if model_path not in MODEL_CACHE:
            MODEL_CACHE[model_path] = load_model(model_path)

        model = MODEL_CACHE[model_path]

        # Load labels
        with open(label_path, "r") as f:
            label_data = json.load(f)

        labels = label_data["labels"]

    except Exception as e:
        print("❌ Error loading model/labels:", e)
        return "Not Predictable", 0.0

    # ✅ Preprocess image directly from MEMORY
    image = preprocess_image(image_bytes)

    # Predict
    preds = model.predict(image, verbose=0)[0]

    index = int(np.argmax(preds))
    confidence = round(float(preds[index]) * 100, 2)

    disease = labels.get(str(index), "Unknown").strip().title()

    # ✅ Disease confidence threshold
    if confidence < 30:
        return "Not Predictable", confidence

    return disease, confidence
