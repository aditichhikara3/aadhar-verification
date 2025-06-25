import cv2
import numpy as np
import dlib
from PIL import Image

# Load face detector
face_detector = dlib.get_frontal_face_detector()


def extract_photo(image_path):
    """
    Detects the largest face in the image and returns a cropped face image (numpy array).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read image: " + image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray, 1)

    if len(faces) == 0:
        raise ValueError("No face detected in ID image.")

    # Choose largest face
    largest_face = max(faces, key=lambda rect: rect.width() * rect.height())
    x, y, w, h = (largest_face.left(), largest_face.top(), largest_face.width(), largest_face.height())

    # Add padding around face
    pad = int(0.25 * h)
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)

    face_img = img[y1:y2, x1:x2]
    return face_img
