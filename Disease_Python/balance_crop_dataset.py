import os
import random

DATASET_PATH = "dataset/crop_dataset"
IMAGE_EXTS = (".jpg", ".jpeg", ".png")
random.seed(42)

def is_image(file):
    return file.lower().endswith(IMAGE_EXTS)

print("🔄 Balancing crop dataset...")

crop_images = {}

for crop in os.listdir(DATASET_PATH):
    crop_path = os.path.join(DATASET_PATH, crop)
    if not os.path.isdir(crop_path):
        continue

    images = [f for f in os.listdir(crop_path) if is_image(f)]
    crop_images[crop] = images

print("📊 Before balancing:",
      {k: len(v) for k, v in crop_images.items()})

min_count = min(len(v) for v in crop_images.values())
print(f"⚖️ Balancing each crop to {min_count} images")

for crop, images in crop_images.items():
    crop_path = os.path.join(DATASET_PATH, crop)
    random.shuffle(images)

    for img in images[min_count:]:
        os.remove(os.path.join(crop_path, img))

print("✅ Crop dataset balanced successfully")
