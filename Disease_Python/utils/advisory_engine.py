import re
from utils.pdf_search_engine import TNAUPDFSearch
from utils.advisory_alias import ADVISORY_ALIAS
from config import TNAU_PDF_PATH

# ======================================================
# INIT PDF ENGINE (LOAD ONCE)
# ======================================================
pdf_engine = TNAUPDFSearch(TNAU_PDF_PATH)

# Keyword banks (relaxed but meaningful)
CAUSE_KEYS = [
    "cause", "caused", "due to", "pathogen", "infection",
    "fungus", "bacteria", "virus", "xanthomonas",
    "puccinia", "ustilaginoidea"
]

SOLUTION_KEYS = [
    "control", "management", "prevent",
    "remove", "spray", "apply", "treat"
]

MEDICINE_KEYS = [
    "@", "g/", "ml/", "kg/ha", "spray",
    "apply", "dose", "wp", "ec"
]


# ======================================================
# FIND DISEASE SECTION USING ALIAS
# ======================================================
def find_disease_section(crop, disease):
    disease_key = disease.lower().strip()

    # Healthy leaf → no advisory
    if "healthy" in disease_key:
        return None

    aliases = ADVISORY_ALIAS.get(disease_key)
    if not aliases:
        return None

    # 🔹 Always search crop + main alias
    text = pdf_engine.search(crop, aliases[0])
    if not text:
        return None

    lines = text.split("\n")
    section = []
    capture = False

    for line in lines:
        l = line.lower()

        # Start when disease alias found
        if any(a in l for a in aliases):
            capture = True

        if capture:
            section.append(line)

    return "\n".join(section).strip() if section else None


# ======================================================
# MEDICINE EXTRACTION
# ======================================================
def extract_medicine_lines(text):
    medicines = []

    for line in text.split("\n"):
        l = line.lower()
        if len(l) < 10:
            continue

        if any(k in l for k in MEDICINE_KEYS):
            medicines.append(line.strip())

    return medicines[:3]


def parse_medicine(line):
    # Extract dosage
    dose = re.search(
        r"([\d\.]+\s*(g|kg|ml)\s*/?\s*(l|ha)?)",
        line.lower()
    )

    dosage = dose.group(1) if dose else "As per TNAU recommendation"

    # Clean medicine name
    name = re.split(
        r"@|spray|apply|dose|wp|ec",
        line,
        flags=re.I
    )[0].strip()

    return f"{name.capitalize()} – {dosage}"


# ======================================================
# MAIN ADVISORY FUNCTION
# ======================================================
def generate_advisory(crop, disease):
    disease_key = disease.lower().strip()

    # ---------------- HEALTHY ----------------
    if "healthy" in disease_key:
        return {
            "cause": "No disease detected in the uploaded crop image.",
            "solution": "Maintain proper crop nutrition and field hygiene.",
            "medicine": "No chemical treatment required."
        }

    disease_text = find_disease_section(crop, disease)

    # ---------------- FALLBACK ----------------
    if not disease_text or len(disease_text) < 30:
        return {
            "cause": "Disease cause information not clearly available in TNAU guide.",
            "solution": "Follow general crop protection and sanitation practices.",
            "medicine": "Consult agriculture officer for appropriate treatment."
        }

    # ---------------- CAUSE ----------------
    cause_lines = [
        line for line in disease_text.split("\n")
        if any(k in line.lower() for k in CAUSE_KEYS)
    ]

    # ---------------- SOLUTION ----------------
    solution_lines = [
        line for line in disease_text.split("\n")
        if any(k in line.lower() for k in SOLUTION_KEYS)
    ]

    # ---------------- MEDICINE ----------------
    medicine_lines = extract_medicine_lines(disease_text)
    medicines = [parse_medicine(l) for l in medicine_lines]

    # ---------------- FINAL SAFE OUTPUT ----------------
    return {
        "cause": " ".join(cause_lines).strip() or
            "The disease is caused by a pathogenic organism as per TNAU advisory.",

        "solution": " ".join(solution_lines).strip() or
            "Follow TNAU recommended disease management practices.",

        "medicine": "\n".join(medicines).strip() or
            "Chemical control details are not specified in the TNAU guide."
    }
