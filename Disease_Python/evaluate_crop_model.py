import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ===============================
# PATHS
# ===============================
DATASET_PATH = "dataset/crop_dataset"
MODEL_PATH = "models/crop_classifier.h5"

# ===============================
# SETTINGS
# ===============================
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ===============================
# LOAD MODEL
# ===============================
model = load_model(MODEL_PATH)

# ===============================
# DATA GENERATOR (NO SHUFFLE)
# ===============================
datagen = ImageDataGenerator(rescale=1./255)

data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# ===============================
# PREDICTION
# ===============================
preds = model.predict(data)
y_pred = np.argmax(preds, axis=1)
y_true = data.classes

# ===============================
# CONFUSION MATRIX
# ===============================
cm = confusion_matrix(y_true, y_pred)

labels = [k for k, v in sorted(data.class_indices.items(), key=lambda x: x[1])]

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(cmap="Blues", xticks_rotation=45)
plt.title("Crop Classification – Confusion Matrix")
plt.tight_layout()
plt.show()
