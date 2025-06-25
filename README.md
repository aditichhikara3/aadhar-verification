# Aadhar-Based Age and Identity Verification System

This project is a web application that performs automated *age verification* and *face matching* using an uploaded Aadhar card (image or PDF) and a live selfie. It checks whether the user is 18+ and if the Aadhar document matches the selfie image using facial recognition.

---

## 🚀 Features

- Upload Aadhar card in .jpg, .png, or .pdf format
- Capture selfie using webcam
- OCR-based extraction of *DOB* from Aadhar
- Extract face from Aadhar and match with selfie
- Check if user is *18+*
- Detect image quality issues (blur, brightness)
- Clear decision: ✅ Accepted / ❌ Rejected
- Confidence percentage for match
- Logs all verification attempts

---

## 🧱 Project Structure

.
├── main.py # Main Flask application
├── templates/index.html # Frontend UI
├── utils/ # Helper modules
│ ├── age_checker.py
│ ├── face_matcher.py
│ ├── image_quality.py
│ ├── ocr_photo_extractor.py
│ ├── ocr_regex_extractor.py
├── models/ # dlib models
│ ├── shape_predictor_68_face_landmarks.dat
│ └── dlib_face_recognition_resnet_model_v1.dat
├── logs/attempts.json # Output logs
├── requirements.txt
└── run.sh


---

## 🛠 Setup Instructions

### 1. Clone the Repository
git clone https://github.com/yourusername/aadhar-verification-app.git
cd aadhar-verification-app

### 2. Install Python Environment (Linux + WSL recommended)

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 3. Install Tesseract OCR
For Ubuntu (WSL or Linux):

sudo apt update
sudo apt install tesseract-ocr

### 4. Run the App Locally

python app.py
Go to http://127.0.0.1:5000 in your browser.

### 🧪 Sample Output

{
  "status": "✅ Accepted",
  
  "message": "Accepted: ID and selfie match with sufficient confidence.",
  
  "confidence": "87.21% match",
  
  "dob": "2004-09-03",
  
  "age": 20,
  
  "is_18_plus": true,
  
  "is_face_match": true,
  
  "quality_feedback": [],
  
  "verified": true
  
}
