from werkzeug.datastructures import FileStorage

from src.classifiers import DrivingLicenseClassifier, BankStatementClassifier, InvoiceClassifier
from src.enums.document_types import DocumentType


def classify_file(file: FileStorage):
    classifiers = [DrivingLicenseClassifier(), BankStatementClassifier(), InvoiceClassifier()]

    for classifier in classifiers:
        document_type = classifier.classify(file=file)

    if document_type:
        return document_type

    return DocumentType.UNKNOWN_FILE.value





