from werkzeug.datastructures.file_storage import FileStorage

import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

import numpy as np
from PIL import Image


def get_img_pieces(
    input_img: FileStorage,
    result_landmarks: list[list[NormalizedLandmark]],
    landmarks_to_extract: list,
) -> list:
    return []


def get_face_landmark_img(input_img: FileStorage) -> list:
    options = vision.FaceLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path='./tasks/face_landmarker.task'
        ),
        num_faces=1,
    )
    detector = vision.FaceLandmarker.create_from_options(options)

    # Image converting sequence
    # `input.img` -> PIL -> Numpy -> MediaPipe -> `converted_input_img`
    converted_input_img = Image.open(input_img.stream)
    converted_input_img = np.array(converted_input_img)
    converted_input_img = mp.Image(
        image_format=mp.ImageFormat.SRGB, data=converted_input_img
    )

    detection_result: vision.FaceLandmarkerResult = detector.detect(
        converted_input_img
    )
    face_landmark_img: list = get_img_pieces(
        input_img=input_img,
        result_landmarks=detection_result.face_landmarks,
        landmarks_to_extract=[
            mp.solutions.face_mesh.FACEMESH_LEFT_EYE,
            mp.solutions.face_mesh.FACEMESH_RIGHT_EYE,
            mp.solutions.face_mesh.FACEMESH_NOSE,
            mp.solutions.face_mesh.FACEMESH_LIPS,
            mp.solutions.face_mesh.FACEMESH_CONTOURS,
            mp.solutions.face_mesh.FACEMESH_IRISES,
        ],
    )

    return face_landmark_img
