import base64
import io

from flask import Flask, render_template, request, send_file, session

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from utils.crop_predict import predict_crop
from utils.disease_predict import predict_disease
from utils.advisory_engine import generate_advisory
from config import DISEASE_MODEL_MAP, ALLOWED_EXTENSIONS

# ==============================
# APP INITIALIZATION
# ==============================
app = Flask(__name__)
app.secret_key = "plant_disease_advisory_secret"  # required for session

# ==============================
# HELPERS
# ==============================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================
# ROUTES
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # 1️⃣ Validate file
        file = request.files.get("leaf")

        if not file or file.filename == "":
            return render_template("index.html", error="No file uploaded")

        if not allowed_file(file.filename):
            return render_template("index.html", error="Invalid file format")

        # 2️⃣ Read image into memory (NO SAVE)
        image_bytes = file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # 3️⃣ STAGE 1: Crop Prediction
        crop, crop_conf = predict_crop(image_bytes)
        crop = crop.lower().strip()

        print("RAW CROP:", crop, crop_conf)

        if crop == "unknown" or crop not in DISEASE_MODEL_MAP:
            return render_template(
                "result.html",
                crop="Unknown",
                disease="Not Predictable",
                crop_conf=crop_conf,
                disease_conf=0.0,
                advisory={
                    "cause": "Crop not supported or image unclear.",
                    "solution": "Please upload a clear leaf image.",
                    "medicine": "N/A"
                },
                image_base64=image_base64
            )

        # 4️⃣ STAGE 2: Disease Prediction
        model_path, label_path = DISEASE_MODEL_MAP[crop]
        disease, disease_conf = predict_disease(image_bytes, model_path, label_path)

        if disease == "Not Predictable":
            return render_template(
                "result.html",
                crop=crop.title(),
                disease="Not Predictable",
                crop_conf=crop_conf,
                disease_conf=disease_conf,
                advisory={
                    "cause": "Disease could not be identified confidently.",
                    "solution": "Try uploading a clearer image.",
                    "medicine": "N/A"
                },
                image_base64=image_base64
            )

        # 5️⃣ STAGE 3: Advisory from TNAU PDF
        advisory = generate_advisory(crop, disease)

        # Save data for PDF download
        session["crop"] = crop.title()
        session["disease"] = disease
        session["advisory"] = advisory

        # ✅ SUCCESS
        return render_template(
            "result.html",
            crop=crop.title(),
            disease=disease,
            crop_conf=crop_conf,
            disease_conf=disease_conf,
            advisory=advisory,
            image_base64=image_base64
        )

    return render_template("index.html")


# ==============================
# DOWNLOAD PRESCRIPTION PDF
# ==============================
@app.route("/download_prescription")
def download_prescription():

    crop = session.get("crop", "N/A")
    disease = session.get("disease", "N/A")
    advisory = session.get("advisory", {})

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Plant Disease Prescription")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Crop    : {crop}")
    pdf.drawString(50, 750, f"Disease : {disease}")

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, 715, "Recommended Advisory (TNAU)")

    pdf.setFont("Helvetica", 11)
    y = 690

    for line in advisory.get("medicine", "").split("\n"):
        pdf.drawString(50, y, line)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = 800

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="plant_disease_prescription.pdf",
        mimetype="application/pdf"
    )

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
