from flask import Flask, request, jsonify

from src.classifier import classify_file
from src.enums.document_types import SupportedFileTypes

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.mimetype in SupportedFileTypes:
        file_class = classify_file(file)
        return jsonify({"file_class": file_class}), 200

    else:
        return jsonify({"error": f"File type not allowed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
