# utils/face_matcher.py
import cv2
import dlib
import numpy as np

# Load models once
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("models/dlib_face_recognition_resnet_model_v1.dat")

def get_face_descriptor(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Could not read image at {image_path}")
        return None

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = face_detector(rgb)
    if len(dets) == 0:
        print("❌ No face detected")
        return None

    shape = shape_predictor(rgb, dets[0])
    descriptor = face_rec_model.compute_face_descriptor(rgb, shape)
    return np.array(descriptor)

def compare_faces(id_face_image, selfie_path):
    try:
        # Save temp ID face for encoding
        id_path = 'temp_id_face.jpg'
        cv2.imwrite(id_path, id_face_image)

        id_desc = get_face_descriptor(id_path)
        self_desc = get_face_descriptor(selfie_path)

        if id_desc is None or self_desc is None:
            return 0.0

        dist = np.linalg.norm(id_desc - self_desc)
        match_score = max(0, 1 - dist)  # lower distance → higher match
        print(f"Match score: {round(match_score * 100, 2)}")
        return match_score
    except Exception as e:
        print(f"Face match error: {e}")
        return 0.0
