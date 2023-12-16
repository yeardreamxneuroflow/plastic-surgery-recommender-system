# import io

from werkzeug.datastructures.file_storage import FileStorage
# from flask import Flask, Response, request, send_file
from flask import Flask, Response, request

import PIL

from face_landmark import get_face_landmark_imgs
from control_marqo import infer_landmarks


app = Flask(__name__)


@app.route('/')
def index() -> str:
    return "<h1>Welcome to Plastic Surgery Recommendation Service Flask \
Application API!</h1>"


@app.route('/recommend', methods=['POST'])
def handle_spring_request() -> Response:
    """Process User Face Image as an Input, Return Multiple Data as an Output

    Returns:
        Data Form:
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
    face_landmark_imgs: list[PIL.Image] = get_face_landmark_imgs(user_img)

    # Infer(search) user landmarks to use marqo
    inference_result: list[list[str, str]] = infer_landmarks(
        face_landmark_imgs)

    # TODO: Return data to use Flask module e.g. Reponse, send_file, etc.
    # return send_file()
