import pdfplumber
import json
import os

# -------------------------------
# PATHS (IMPORTANT)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_PATH = os.path.join(BASE_DIR, "dataset", "tnau_guides", "tnau_advisory.pdf")
OUTPUT_JSON = os.path.join(BASE_DIR, "dataset", "tnau_guides", "advisory_data.json")

data = {}

with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        lines = text.split("\n")

        crop = None
        disease = None

        for line in lines:
            line = line.strip().lower()

            if "crop:" in line:
                crop = line.replace("crop:", "").strip()
                data.setdefault(crop, {})

            elif "disease:" in line:
                disease = (
                    line.replace("disease:", "")
                    .strip()
                    .replace(" ", "_")
                )
                data[crop].setdefault(disease, {
                    "cause": "",
                    "solution": "",
                    "medicine": ""
                })

            elif crop and disease and "cause" in line:
                data[crop][disease]["cause"] += line + " "

            elif crop and disease and ("control" in line or "management" in line):
                data[crop][disease]["solution"] += line + " "

            elif crop and disease and ("spray" in line or "dosage" in line):
                data[crop][disease]["medicine"] += line + " "

# -------------------------------
# SAVE JSON
# -------------------------------
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("JSON created successfully at:")
print(OUTPUT_JSON)

