# utils/image_quality.py
import cv2

def assess_quality(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur detection
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    feedback = []
    if laplacian_var < 100:
        feedback.append("Image appears blurry")

    # Brightness check
    brightness = gray.mean()
    if brightness < 60:
        feedback.append("Image appears too dark")
    elif brightness > 200:
        feedback.append("Image appears too bright")

    return feedback
