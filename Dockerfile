# Use an official Python runtime as the base image
FROM python:3.12-slim

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract for OCR

RUN apt-get update && apt-get -y install tesseract-ocr


# Copy the Flask application code into the container
COPY . .

# Expose the port that Gunicorn will run on
EXPOSE 8080

# Run Gunicorn
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--bind", "0.0.0.0:8080", "src.app:app"]