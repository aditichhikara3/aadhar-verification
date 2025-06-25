Aadhar-based Age & Identity Verification

This application verifies age and identity using an Aadhar image (or PDF) and a live selfie. It
extracts the date of birth, checks if the person is 18+, compares the ID photo with a selfie, and gives
quality feedback.

Features
- OCR for extracting DOB and ID photo.
- Face comparison between Aadhar photo and live selfie.
- Blur and brightness detection on selfies.
- Simple web interface.
- Logs verification attempts.
- Supports Aadhar in image or PDF format.

How to Run (Development)
1. Clone this repository
git clone <your-repo-url>
cd age-id-verification
2. Set up Python Virtual Environment
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Also, install Tesseract-OCR (Linux):
sudo apt update
sudo apt install tesseract-ocr
Make sure these model files exist inside models/:
- shape_predictor_68_face_landmarks.dat
- dlib_face_recognition_resnet_model_v1.dat
If not, download them from Dlib's model zoo.
4. Run the App
python app.py
Visit http://127.0.0.1:5000 in your browser.
Output
On submitting Aadhar + selfie, it shows:
- Verification Status
- Confidence % match
- Age + DOB
- Feedback if selfie is blurry or poorly lit
Logs
All attempts are saved in logs/attempts.json for auditing or analytics.

Build Executable Binary

You can package the app as a standalone executable:
1. Install PyInstaller
pip install pyinstaller
2. Build
pyinstaller --noconfirm --onefile --add-data "templates:templates" --add-data "models:models"
--add-data "static:static" app.py
The binary will be in dist/app.
3. Run the Binary
./dist/app
Notes
- This is a prototype; do not use in production without securing file uploads and improving spoof
detection.
- You may customize quality feedback thresholds in image_quality.py.
