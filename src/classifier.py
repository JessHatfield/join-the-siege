from werkzeug.datastructures import FileStorage

from src.classifiers.daberta_zero_shot_text_classifer import DebertaV3Classifier
from src.enums.document_types import DocumentType


def classify_file(file: FileStorage):
    classifiers = [DebertaV3Classifier()]
    for classifier in classifiers:
        document_type = classifier.classify(file=file)

    if document_type:
        return document_type

    return DocumentType.UNKNOWN_FILE.value
