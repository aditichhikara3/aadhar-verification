import face_recognition
import numpy as np

def compare_faces(id_image, selfie_path):
    id_face_encodings = face_recognition.face_encodings(id_image)
    selfie = face_recognition.load_image_file(selfie_path)
    selfie_encodings = face_recognition.face_encodings(selfie)

    if not id_face_encodings or not selfie_encodings:
        return 0.0

    id_encoding = id_face_encodings[0]
    selfie_encoding = selfie_encodings[0]

    distance = np.linalg.norm(id_encoding - selfie_encoding)
    similarity = 1 - distance  # normalized score
    return max(min(similarity, 1), 0)