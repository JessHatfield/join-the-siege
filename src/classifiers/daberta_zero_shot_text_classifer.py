import dataclasses

from transformers import pipeline
from werkzeug.datastructures import FileStorage

from src.classifiers.base_classifier import DocumentClassifier
from src.classifiers.utils import extract_text_from_file
from src.enums.document_types import DocumentType


class DebertaV3Classifier(DocumentClassifier):

    def __init__(self):
        self.classifier = pipeline(model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
        self.candidate_labels = [doc_type.value for doc_type in DocumentType]

    def classify(self, file: FileStorage) -> DocumentType:
        extracted_text = extract_text_from_file(file, file.mimetype)
        result = self.classifier(extracted_text, self.candidate_labels, multi_label=False)

        return result['labels'][0]
