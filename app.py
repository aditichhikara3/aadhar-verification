from flask import Flask, render_template, request, jsonify
import os
from utils.ocr_utils import extract_dob_and_photo
from utils.face_matcher import compare_faces
from utils.age_checker import calculate_age, is_adult
from utils.image_quality import assess_quality
import json
from datetime import datetime

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
        selfie_file = request.files['selfie']

        # Save temporary files
        aadhar_path = 'temp_aadhar.jpg'
        selfie_path = 'temp_selfie.jpg'
        aadhar_file.save(aadhar_path)
        selfie_file.save(selfie_path)

        # Step 1: Extract DOB and photo
        dob, id_face = extract_dob_and_photo(aadhar_path)
        age = calculate_age(dob) if dob else None
        is_18_plus = is_adult(age)

        # Step 2: Face match
        match_score = compare_faces(id_face, selfie_path)
        is_match = match_score >= 0.7

        # Step 3: Image quality
        quality_issues = assess_quality(selfie_path)

        # Step 4: Build result
        result = {
            "dob": dob,
            "age": age,
            "is_18_plus": is_18_plus,
            "face_match_score": round(match_score * 100, 2),
            "is_face_match": is_match,
            "quality_feedback": quality_issues,
            "verified": is_match and is_18_plus
        }

        # Step 5: Log
        result_with_time = {"timestamp": datetime.utcnow().isoformat(), **result}
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(result_with_time) + '\n')

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Set to False for production
