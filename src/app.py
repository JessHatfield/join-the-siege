from flask import Flask, request, jsonify

from src.classifier import classify_file
from src.enums import SupportedFileTypes

import sentry_sdk

sentry_sdk.init(
    dsn="https://92779b5e7b8a4a3d4dfb846aecde41bc@o4508273926733824.ingest.de.sentry.io/4508273928241232",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

app = Flask(__name__)


def allowed_mimetype(mimetype: str) -> bool:
    if mimetype in SupportedFileTypes:
        return True
    return False


@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if allowed_mimetype(file.mimetype):
        classification_results = classify_file(file)
        file_class = classification_results.get_document_label()
        return jsonify({"file_class": file_class}), 200

    else:
        return jsonify({"error": f"File type not allowed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
