import fitz  # PyMuPDF

class TNAUPDFSearch:
    def __init__(self, pdf_path):
        self.pdf = fitz.open(pdf_path)

    def search(self, crop, disease):
        crop = crop.lower()
        disease = disease.lower()

        matched_text = []

        for page in self.pdf:
            text = page.get_text().lower()

            if crop in text and disease.replace("_", " ") in text:
                matched_text.append(page.get_text())

        if not matched_text:
            return ""

        return "\n".join(matched_text[:3])  # limit pages (performance)
