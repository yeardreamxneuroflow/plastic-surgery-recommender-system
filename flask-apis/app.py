"""Entrypoint of Flask Application.
"""


import io
import time
import base64

import boto3
from flask import Flask, Response, request, jsonify
from werkzeug.datastructures import FileStorage

from PIL import Image

from mediapipe_tools import get_face_landmark_imgs
from marqo_tools import infer_landmarks
from macro import AWSMacro, MediaPipeMacro


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index() -> str:
    """Non-functional view function.
    """

    return "<h1>Welcome to Plastic Surgery Recommendation Service Flask API!</h1>"


@app.route("/scrape", methods=["POST"])
def handle_scrape_request() -> Response:
    """Operate Scraping Pipeline.
    """

    # TODO: Run Scrapy to run scrape-store pipeline
    pass


def upload_face_landmark_imgs(
    user_timestamp: str,
    face_landmark_imgs: list[Image.Image],
) -> None:
    """Store extracted landmark images to S3 Bucket
    """

    aws_macro = AWSMacro()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_macro.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_macro.AWS_SECRET_ACCESS_KEY,
    )
    for landmark_idx, landmark_img in enumerate(face_landmark_imgs):
        if landmark_idx == 0:
            landmark = "left-eye"
        elif landmark_idx == 1:
            landmark = "right-eye"
        elif landmark_idx == 2:
            landmark = "nose"
        elif landmark_idx == 3:
            landmark = "lips"

        img_buffer = io.BytesIO()
        landmark_img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        # Store image to S3 Bucket
        s3.upload_fileobj(
            Fileobj=img_buffer,
            Bucket=aws_macro.AWS_USER_LANDMARK_BUCKET_NAME,
            Key=f"{user_timestamp}/{landmark}.jpg",
        )


@app.route('/recommend', methods=['POST'])
def handle_spring_request() -> Response:
    """Process user face image as an input and multiple data as an output.

    Returns:
        Example of data:
        {
            "landmark_00": {
                1. User's face landmark image
                2. Most similar wannabe
                3. Similarity score
            },
            "landmark_01": {
                1. User's face landmark image
                2. Most similar wannabe
                3. Similarity score
            },
            ...
        }
    """

    mp_macro = MediaPipeMacro()
    output_data = {}

    # Get user's face landmarks
    user_img: FileStorage = request.files["img_file"]
    face_landmark_imgs: list[Image.Image] = get_face_landmark_imgs(user_img)

    # Init data insertion to return value(output_data)
    for landmark_idx, landmark_name in enumerate(mp_macro.Landmark.DEFINED_LANDMARKS):
        # For HTTP Response
        user_landmark_image_b64 = base64.b64encode(
            face_landmark_imgs[landmark_idx].tobytes()).decode()

        output_data[landmark_name] = {
            "user_landmark_image": user_landmark_image_b64,
        }

    # TODO: Replace user_timestamp(Unix Timestamp) to managed user ID
    user_timestamp = str(time.time())

    upload_face_landmark_imgs(user_timestamp, face_landmark_imgs)
    infer_landmarks(user_timestamp, output_data)

    return jsonify(output_data)
