from werkzeug.datastructures.file_storage import FileStorage

import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

import PIL
import numpy as np

import face_landmark_macro


def denormalize_landmark_points(
    pil_img: PIL.Image,
    points_to_denormalize: list[NormalizedLandmark],
) -> None:
    img_width, img_height = pil_img.size

    for _, landmark in enumerate(points_to_denormalize):
        landmark.x = landmark.x * img_width
        landmark.y = landmark.y * img_height


def detect_landmark_points(
    pil_img: PIL.Image,
) -> list[NormalizedLandmark]:
    mp_img = np.array(pil_img)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB,
                      data=mp_img)

    options = vision.FaceLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path='./tasks/face_landmarker.task'
        ),
        num_faces=1,
    )
    detector = vision.FaceLandmarker.create_from_options(options)
    detection_result: vision.FaceLandmarkerResult = detector.detect(mp_img)

    denormalize_landmark_points(pil_img, detection_result.face_landmarks[0])

    return detection_result.face_landmarks[0]


def get_single_landmark_img(
    img: PIL.Image,
    denormalized_landmark_points: list[NormalizedLandmark],
    x1_idx: int,
    y1_idx: int,
    x2_idx: int,
    y2_idx: int,
) -> PIL.Image:
    copied_img_to_crop = img.copy()
    x1: float = denormalized_landmark_points[x1_idx].x
    y1: float = denormalized_landmark_points[y1_idx].y
    x2: float = denormalized_landmark_points[x2_idx].x
    y2: float = denormalized_landmark_points[y2_idx].y

    return copied_img_to_crop.crop((x1, y1, x2, y2))


def get_face_landmark_imgs(input_img: FileStorage) -> list[PIL.Image]:
    """
    Kind of face landmarks
    - Left eye
    - Right eye
    - Nose
    - Lips
    """

    pil_img = PIL.Image.open(input_img.stream)
    detected_landmark_points = detect_landmark_points(pil_img)

    left_eye_img = get_single_landmark_img(
        pil_img,
        detected_landmark_points,
        face_landmark_macro.LEFT_EYE_RIGHT_EDGE,
        face_landmark_macro.LEFT_EYE_TOP_EDGE,
        face_landmark_macro.LEFT_EYE_LEFT_EDGE,
        face_landmark_macro.LEFT_EYE_BOTTOM_EDGE,
    )
    right_eye_img = get_single_landmark_img(
        pil_img,
        detected_landmark_points,
        face_landmark_macro.RIGHT_EYE_RIGHT_EDGE,
        face_landmark_macro.RIGHT_EYE_TOP_EDGE,
        face_landmark_macro.RIGHT_EYE_LEFT_EDGE,
        face_landmark_macro.RIGHT_EYE_BOTTOM_EDGE,
    )
    nose_img = get_single_landmark_img(
        pil_img,
        detected_landmark_points,
        face_landmark_macro.NOSE_LEFT_EDGE,
        face_landmark_macro.NOSE_TOP_EDGE,
        face_landmark_macro.NOSE_RIGHT_EDGE,
        face_landmark_macro.NOSE_BOTTOM_EDGE,
    )
    lips_img = get_single_landmark_img(
        pil_img,
        detected_landmark_points,
        face_landmark_macro.LIPS_LEFT_EDGE,
        face_landmark_macro.LIPS_TOP_EDGE,
        face_landmark_macro.LIPS_RIGHT_EDGE,
        face_landmark_macro.LIPS_BOTTOM_EDGE,
    )
    # # Idea: Extract 'face oval'(얼굴윤곽)
    # face_oval_img: Image = get_single_landmark_img(
    #     pil_input_img,
    #     result_landmarks,
    #     face_landmark_macro.FACE_OVAL_LEFT_EDGE,
    #     face_landmark_macro.FACE_OVAL_RIGHT_EDGE,
    #     face_landmark_macro.FACE_OVAL_TOP_EDGE,
    #     face_landmark_macro.FACE_OVAL_BOTTOM_EDGE,
    # )

    return [left_eye_img, right_eye_img, nose_img, lips_img]
