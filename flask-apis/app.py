"""Entrypoint of Flask Application.
"""


from typing import List

from flask import Flask, Response, request
from werkzeug.datastructures import FileStorage

from PIL import Image

from mediapipe_tools import get_face_landmark_imgs
from marqo_tools import infer_landmarks


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


@app.route('/recommend', methods=['POST'])
def handle_spring_request() -> Response:
    """Process user face image as an input and multiple data as an output.

    Returns:
        Example of data:
        [
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
        ]
    """

    # Get user's face landmarks
    user_img: FileStorage = request.files["img_file"]
    face_landmark_imgs: List[Image.Image] = get_face_landmark_imgs(user_img)

    # Searching user landmarks from marqo
    inference_result: List[List[str, str]] = infer_landmarks(
        face_landmark_imgs)

    # TODO: Return multiple data to use Flask module
