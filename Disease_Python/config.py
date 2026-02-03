# Allowed image formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# TNAU PDF path
TNAU_PDF_PATH = "dataset/tnau_guides/AGRICULTURE.pdf"

# Disease model map
DISEASE_MODEL_MAP = {
    "tomato": (
        "models/disease_models/tomato_dataset_disease.h5",
        "labels/tomato_dataset_labels.json"
    ),
    "potato": (
        "models/disease_models/potato_dataset_disease.h5",
        "labels/potato_dataset_labels.json"
    ),
    "pepper": (
        "models/disease_models/pepper_dataset_disease.h5",
        "labels/pepper_dataset_labels.json"
    ),
    "rice": (
        "models/disease_models/rice_dataset_disease.h5",
        "labels/rice_dataset_labels.json"
    ),
    "sugarcane": (
        "models/disease_models/sugarcane_dataset_disease.h5",
        "labels/sugarcane_dataset_labels.json"
    )
}
