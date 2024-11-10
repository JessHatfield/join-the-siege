# Use an official Python runtime as the base image
FROM python:3.12-slim

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract for OCR and git-lfs

RUN apt-get update && apt-get -y install tesseract-ocr


# Copy the Flask application code into the container
COPY . .

# Download our models - We use a bash script here as the cli is prone to ChunkedEncodingErrors!
RUN timeout 180 bash -c 'while ! huggingface-cli download MoritzLaurer/deberta-v3-large-zeroshot-v2.0; do sleep 1; done'


# Expose the port that Gunicorn will run on
EXPOSE 8080

# Run Gunicorn
CMD ["gunicorn","--workers","4", "--access-logfile", "-", "--error-logfile", "-", "--bind", "0.0.0.0:8080", "src.app:app"]