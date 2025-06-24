import pytesseract
import cv2
import re
from PIL import Image

def extract_dob_and_photo(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    dob_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})', text)
    dob = dob_match.group(0) if dob_match else None

    # Fake crop: return whole image as placeholder for ID photo
    return dob, image