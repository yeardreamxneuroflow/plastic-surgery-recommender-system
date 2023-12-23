from typing import Union, List
from werkzeug.datastructures.file_storage import FileStorage

import io

import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

from PIL import Image
import numpy as np

import boto3

import face_landmark_macro
from aws_macro import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# TODO: Change bucket name when scraping pipeline is made
from aws_macro import AWS_MANUAL_WANNABE_BUCKET_NAME


def denormalize_landmark_points(
    pil_img: Image.Image,
    points_to_denormalize: list[NormalizedLandmark],
) -> None:
    img_width, img_height = pil_img.size

    for _, landmark in enumerate(points_to_denormalize):
        landmark.x = landmark.x * img_width
        landmark.y = landmark.y * img_height


def detect_landmark_points(
    pil_img: Image.Image,
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
    img: Image.Image,
    denormalized_landmark_points: list[NormalizedLandmark],
    x1_idx: int,
    y1_idx: int,
    x2_idx: int,
    y2_idx: int,
) -> Image.Image:
    copied_img_to_crop = img.copy()
    x1: float = denormalized_landmark_points[x1_idx].x
    y1: float = denormalized_landmark_points[y1_idx].y
    x2: float = denormalized_landmark_points[x2_idx].x
    y2: float = denormalized_landmark_points[y2_idx].y

    return copied_img_to_crop.crop((x1, y1, x2, y2))


# TODO: Fix `AttributeError` to Use Type Hint using `Union`
def get_face_landmark_imgs(input_img: Union[Image.Image, FileStorage]) -> list[Image.Image]:
    """
    Kind of face landmarks
    - Left eye
    - Right eye
    - Nose
    - Lips
    """

    if __name__ == "__main__":  # Method was called manually
        pil_img = input_img
    elif __name__ != "__main__":
        pil_img = Image.open(input_img.stream)

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


def extract_landmarks_manually(wannabe_list: List[str]):
    """Extract Wannabe Image's Landmarks and Store to S3 Bucket
    """

    # AWS S3 client to store extracted landmark images
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    for wannabe in wannabe_list:
        r: list[Image.Image] = get_face_landmark_imgs(Image.open(
            f"manual_images/{wannabe}/original.jpg"))

        for img_idx, img in enumerate(r):
            if img_idx == 0:
                landmark = "left-eye"
            elif img_idx == 1:
                landmark = "right-eye"
            elif img_idx == 2:
                landmark = "nose"
            elif img_idx == 3:
                landmark = "lips"

            # Create BytesIO Object
            img_obj = io.BytesIO()

            # Save Image to the Object
            img.save(img_obj, format="JPEG")

            # Seek Object
            img_obj.seek(0)

            # Store image to S3 Bucket
            s3.upload_fileobj(
                Fileobj=img_obj,
                Bucket=AWS_MANUAL_WANNABE_BUCKET_NAME,
                Key=f"{wannabe}/{landmark}.jpg",
            )


# Manual Landmark Extraction and Store
if __name__ == "__main__":
    wannabe_list = [
        "박보검",
        "뷔",
        "서강준",
        "송강",
        "송중기",
        "신세경",
        "아이린",
        "아이유",
        "오연서",
        "윈터",
        "육성재",
        "윤아",
        "이주빈",
        "장원영",
        "정국",
        "정우성",
        "제니",
        "차은우",
        "카리나",
    ]

    extract_landmarks_manually(
        wannabe_list=wannabe_list,
    )
