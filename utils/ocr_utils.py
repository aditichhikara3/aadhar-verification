import re
import cv2
import pytesseract
from PIL import Image
import numpy as np
from datetime import datetime

def extract_dob_and_photo(aadhar_path):
    # Read image and preprocess
    image = cv2.imread(aadhar_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to clean noise
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # OCR extract
    text = pytesseract.image_to_string(processed)
    print("🔍 OCR Text:\n", text)

    # Try to find DOB using loose regex (DD-MM-YYYY or DD/MM/YYYY)
    dob_match = re.search(r'(\d{2}[-/]\d{2}[-/]\d{4})', text)
    dob_str = dob_match.group(1) if dob_match else None

    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, "%d-%m-%Y")
        except ValueError:
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y")
            except ValueError:
                pass

    # Extract ID face
    h, w = image.shape[:2]
    id_face = image[h//4:h//2, w//10:w//4]  # crude crop, you can refine this later

    return dob, id_face
