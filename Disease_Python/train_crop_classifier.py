import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ===============================
# PATHS
# ===============================
DATASET_DIR = "dataset/crop_dataset"
MODEL_SAVE_PATH = "models/crop_classifier.h5"
LABEL_SAVE_PATH = "labels/crop_labels.json"

# ✅ Create folders BEFORE training
os.makedirs("models", exist_ok=True)
os.makedirs("labels", exist_ok=True)

# ===============================
# SETTINGS
# ===============================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS_INITIAL = 20
EPOCHS_FINE_TUNE = 10
CONFIDENCE_THRESHOLD = 0.75   # ⭐ 75% CONFIDENCE RULE

# ===============================
# DATA GENERATOR
# ===============================
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

print("✅ Crop class indices:", train_data.class_indices)

# ===============================
# MODEL: MobileNetV2
# ===============================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Stage 1 – freeze base model
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# ===============================
# COMPILE – STAGE 1
# ===============================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ===============================
# CALLBACKS
# ===============================
callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    )
]

# ===============================
# TRAIN – STAGE 1
# ===============================
print("🚀 Training crop classifier (top layers)...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_INITIAL,
    callbacks=callbacks
)

# ===============================
# FINE-TUNING – STAGE 2
# ===============================
print("🔓 Fine-tuning MobileNetV2...")

base_model.trainable = True

# Freeze all except last 30 layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_FINE_TUNE,
    callbacks=callbacks
)

# ===============================
# SAVE MODEL & LABELS + CONFIDENCE
# ===============================
model.save(MODEL_SAVE_PATH)

# 🔥 index → crop mapping (FIXED & SAFE)
index_to_crop = {str(v): k for k, v in train_data.class_indices.items()}

label_data = {
    "labels": index_to_crop,
    "confidence_threshold": CONFIDENCE_THRESHOLD
}

with open(LABEL_SAVE_PATH, "w") as f:
    json.dump(label_data, f, indent=4)

print("--------------------------------------------------")
print("✅ Crop classifier saved at:", MODEL_SAVE_PATH)
print("✅ Crop labels + 75% confidence saved at:", LABEL_SAVE_PATH)
print("--------------------------------------------------")
