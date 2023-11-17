import io

from flask import request, Flask, send_file, Response


app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'Flask Application to return recommend image'


def compose_images(input_img: bytes, wannabe_img: bytes) -> bytes:
    return input_img  # Temporary return value


@app.route('/recommend', methods=['POST'])
def handle_request() -> Response:
    input_img = request.files['img_file'].read()
    wannabe_img = None
    output_img = compose_images(input_img, wannabe_img)

    return send_file(io.BytesIO(output_img),
                     download_name='composition_image')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
