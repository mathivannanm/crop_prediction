import os
import sys
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ==================================================
# USAGE
# python train_disease_model.py tomato
# python train_disease_model.py potato
# python train_disease_model.py pepper
# ==================================================

if len(sys.argv) != 2:
    print("❌ Usage: python train_disease_model.py <crop_name>")
    sys.exit(1)

crop = sys.argv[1].lower()

# ==================================================
# PATHS
# ==================================================
DATASET_DIR = f"dataset/{crop}"
MODEL_SAVE_PATH = f"models/disease_models/{crop}_disease.h5"
LABEL_SAVE_PATH = f"labels/{crop}_labels.json"

# ==================================================
# SETTINGS
# ==================================================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS_INITIAL = 20
EPOCHS_FINE_TUNE = 10
CONFIDENCE_THRESHOLD = 0.75   # ⭐ 75% CONFIDENCE RULE

# ==================================================
# CHECK DATASET
# ==================================================
if not os.path.isdir(DATASET_DIR):
    print(f"❌ Dataset folder not found: {DATASET_DIR}")
    sys.exit(1)

# ==================================================
# DATA GENERATOR
# ==================================================
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

print(f"✅ {crop} disease labels:", train_data.class_indices)

# ==================================================
# MODEL – MobileNetV2 (TRANSFER LEARNING)
# ==================================================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Stage 1: Freeze base model
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# ==================================================
# COMPILE – STAGE 1
# ==================================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ==================================================
# CALLBACKS
# ==================================================
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

# ==================================================
# TRAIN – STAGE 1
# ==================================================
print(f"🚀 Training {crop} disease model (top layers)...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_INITIAL,
    callbacks=callbacks
)

# ==================================================
# FINE-TUNING – STAGE 2
# ==================================================
print("🔓 Fine-tuning last layers of MobileNetV2...")

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

# ==================================================
# SAVE MODEL & LABELS WITH CONFIDENCE
# ==================================================
os.makedirs("models/disease_models", exist_ok=True)
os.makedirs("labels", exist_ok=True)

# Save model
model.save(MODEL_SAVE_PATH)

# Save labels + confidence threshold
labels = {v: k for k, v in train_data.class_indices.items()}

label_data = {
    "labels": labels,
    "confidence_threshold": CONFIDENCE_THRESHOLD
}

with open(LABEL_SAVE_PATH, "w") as f:
    json.dump(label_data, f, indent=4)

print("--------------------------------------------------")
print(f"✅ {crop} disease model saved at: {MODEL_SAVE_PATH}")
print(f"✅ Labels + 75% confidence saved at: {LABEL_SAVE_PATH}")
print("--------------------------------------------------")
