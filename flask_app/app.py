import io

from werkzeug.datastructures.file_storage import FileStorage
from flask import Flask, Response, request, send_file

import PIL

from face_landmark import get_face_landmark_imgs
from image_vectorization import vectorize_img
from wannabe_image import get_most_similar_wannabe_img
from image_generation import generate_image


app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'Flask Application to return recommend image...'


@app.route('/recommend', methods=['POST'])
def handle_request() -> Response:
    input_img: FileStorage = request.files['img_file']
    face_landmark_imgs: list[PIL.Image] = get_face_landmark_imgs(input_img)
    vectorized_landmakrs = vectorize_img(face_landmark_imgs)
    most_similar_wannabe_img = get_most_similar_wannabe_img(
        vectorized_landmakrs
    )
    output_img = generate_image(input_img, most_similar_wannabe_img)

    return send_file(
        io.BytesIO(output_img),
        download_name='output_img_file'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
