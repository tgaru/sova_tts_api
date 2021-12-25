from base64 import b64encode

from flask import Flask, render_template, request, send_from_directory, url_for, send_file
from flask_cors import CORS, cross_origin

from models import models, ALL_MODELS
from file_handler import FileHandler


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

_valid_model_types = [key for key in models if key is not ALL_MODELS]


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return render_template("speechSynthesis.html", existing_models=models.keys())


@app.route("/synthesize/", methods=["POST"])
@cross_origin()
def synthesize():
    text = request.form['text']

    options = {
        "rate": float(1.0),
        "pitch": float(1.0),
        "volume": float(0.0)
    }

    response_code, results = FileHandler.get_synthesized_audio(text, 'Ruslan', **options)


    path_to_file = results[0]['pathfile']

    return send_file(
        path_to_file,
        mimetype="audio/wav",
        as_attachment=False,
        attachment_filename='speech.wav')
    return {
        "response_code": response_code,
        "response": results[0]
    }


if __name__ == "__main__":
    app.run(debug=True)
