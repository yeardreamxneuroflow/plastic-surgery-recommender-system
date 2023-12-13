import io

from werkzeug.datastructures.file_storage import FileStorage
from flask import Flask, Response, request, send_file

import PIL

from face_landmark import get_face_landmark_imgs


app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'Flask Application to return recommend image...'


@app.route('/recommend', methods=['POST'])
def handle_request() -> Response:
    input_img: FileStorage = request.files['img_file']
    face_landmark_imgs: list[PIL.Image] = get_face_landmark_imgs(input_img)

    return send_file(
        io.BytesIO(output_img),
        download_name='output_img_file'
    )
