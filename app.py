from flask import Flask, render_template, request, jsonify
import os
import json
import base64
import cv2
import pytesseract
from datetime import datetime
from pdf2image import convert_from_path

from utils.ocr_regex_extractor import extract_dob_from_text
from utils.ocr_photo_extractor import extract_photo
from utils.age_checker import calculate_age, is_adult
from utils.face_matcher import compare_faces
from utils.image_quality import assess_quality

app = Flask(__name__)

LOG_FILE = 'logs/attempts.json'
os.makedirs('logs', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    try:
        aadhar_file = request.files['aadhar']
        selfie_data_url = request.form['selfie_data']

        # Save selfie from base64
        selfie_data = selfie_data_url.split(',')[1]
        selfie_path = 'temp_selfie.jpg'
        with open(selfie_path, "wb") as f:
            f.write(base64.b64decode(selfie_data))

        # Handle Aadhar input (PDF or image)
        aadhar_path = 'temp_aadhar.jpg'
        if aadhar_file.filename.lower().endswith('.pdf'):
            aadhar_file.save('temp_aadhar.pdf')
            pages = convert_from_path('temp_aadhar.pdf')
            pages[0].save(aadhar_path, 'JPEG')
        else:
            aadhar_file.save(aadhar_path)

        # ✅ Step 1: OCR + DOB extraction using regex logic
        img = cv2.imread(aadhar_path)
        text = pytesseract.image_to_string(img)
        print("🔍 OCR Text:\n", text)
        dob = extract_dob_from_text(text)

        # ✅ Step 2: ID face extraction
        id_face = extract_photo(aadhar_path)

        # ✅ Step 3: Age check
        age = calculate_age(dob) if dob else None
        is_18_plus = is_adult(age)

        # ✅ Step 4: Face match
        match_score = compare_faces(id_face, selfie_path)
        is_match = match_score >= 0.55

        # ✅ Step 5: Image quality
        quality_issues = assess_quality(selfie_path)

        # ✅ Step 6: Build result
        feedback_reasons = []
        status = "✅ Accepted"
        message = "Accepted: ID and selfie match with sufficient confidence."

        if not is_match:
            feedback_reasons.append("Photo does not match the ID.")
        if not is_18_plus:
            feedback_reasons.append("User is below 18 years old.")
        if quality_issues:
            feedback_reasons.extend(quality_issues)

        if feedback_reasons:
            status = "❌ Rejected"
            message = "Rejected: " + " ".join(feedback_reasons)

        result = {
            "status": status,
            "message": message,
            "confidence": f"{round(match_score * 100, 2)}% match",
            "dob": dob.strftime("%Y-%m-%d") if dob else None,
            "age": int(age) if age is not None else None,
            "is_18_plus": bool(is_18_plus),
            "face_match_score": float(round(match_score * 100, 2)),
            "is_face_match": bool(is_match),
            "quality_feedback": quality_issues,
            "verified": bool(is_match and is_18_plus)
        }

        # ✅ Step 7: Log
        result_with_time = {"timestamp": datetime.utcnow().isoformat(), **result}
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(result_with_time) + '\n')

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
