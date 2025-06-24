import cv2
import numpy as np
import face_recognition


def assess_quality(image_path):
    feedback = []
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blurriness check
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 100:
        feedback.append("Image is blurry, try holding camera steady")

    # Brightness check
    brightness = np.mean(gray)
    if brightness < 60:
        feedback.append("Too dark, please increase lighting")

    # Face presence check
    faces = face_recognition.face_locations(image)
    if not faces:
        feedback.append("No face detected, please retake selfie")

    return feedback