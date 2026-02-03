import os
import random

DATASET_PATH = "dataset"
IMAGE_EXTS = (".jpg", ".jpeg", ".png")
random.seed(42)

def is_image(file):
    return file.lower().endswith(IMAGE_EXTS)

print("🔄 Balancing disease datasets...")

for crop in os.listdir(DATASET_PATH):

    # 🚨 Skip crop dataset
    if crop == "crop_dataset":
        continue

    crop_path = os.path.join(DATASET_PATH, crop)
    if not os.path.isdir(crop_path):
        continue

    disease_images = {}

    for disease in os.listdir(crop_path):
        disease_path = os.path.join(crop_path, disease)
        if not os.path.isdir(disease_path):
            continue

        images = [f for f in os.listdir(disease_path) if is_image(f)]
        disease_images[disease] = images

    if not disease_images:
        continue

    print(f"\n📊 {crop} before balancing:",
          {k: len(v) for k, v in disease_images.items()})

    min_count = min(len(v) for v in disease_images.values())
    print(f"⚖️ Balancing {crop} diseases to {min_count} images")

    for disease, images in disease_images.items():
        disease_path = os.path.join(crop_path, disease)
        random.shuffle(images)

        for img in images[min_count:]:
            os.remove(os.path.join(disease_path, img))

    print(f"✅ {crop} disease dataset balanced")

print("\n🎯 All disease datasets balanced successfully")
